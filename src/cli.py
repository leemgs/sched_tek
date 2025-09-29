import argparse, json
from dataclasses import asdict
from .telemetry import gather
from .kb import KnowledgeBase
from .reasoning import recommend
from .safety import SafeAction
from .rollout import apply
from .monitor import check
from . import eval as evalmod

def main():
    ap = argparse.ArgumentParser(prog="sched_tek_cli")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_tel = sub.add_parser("telemetry")
    ap_tel.add_argument("--workload", default=None)

    ap_rec = sub.add_parser("recommend")
    ap_rec.add_argument("--slo-p95-ms", type=float, default=120.0)
    ap_rec.add_argument("--workload", default=None)

    ap_apply = sub.add_parser("apply")
    ap_apply.add_argument("--slo-p95-ms", type=float, default=120.0)
    ap_apply.add_argument("--workload", default=None)
    ap_apply.add_argument("--dry-run", type=int, default=1)  # 1=sandbox (default), 0=allow live if env permits

    ap_mon = sub.add_parser("monitor")
    ap_mon.add_argument("--workload", default=None)

    ap_eval = sub.add_parser("eval")
    ap_eval.add_argument("--trials", type=int, default=10)
    ap_eval.add_argument("--report", choices=["curve","energy","ablation"], default=None)

    args = ap.parse_args()
    kb = KnowledgeBase("configs/knowledge_base.json")

    if args.cmd == "telemetry":
        tel = gather(args.workload)
        print(json.dumps(asdict(tel), indent=2))
    elif args.cmd == "recommend":
        tel = gather(args.workload)
        recs = recommend(kb, tel, slo_p95_ms=args.slo_p95_ms)
        print(json.dumps([asdict(r) for r in recs], indent=2))
    elif args.cmd == "apply":
        tel = gather(args.workload)
        recs = recommend(kb, tel, slo_p95_ms=args.slo_p95_ms)
        acts = [SafeAction(param=r.param, value=r.target) for r in recs]
        if args.dry_run == 1:
            # Force sandbox by clearing LIVE_APPLY
            import os
            os.environ["LIVE_APPLY"] = "0"
        notes = apply(kb, acts)
        print("\n".join(notes))
    elif args.cmd == "monitor":
        rep = check(args.workload)
        print(f"{'OK' if rep.ok else 'ATTN'}: {rep.msg}")
    elif args.cmd == "eval":
        res = evalmod.run(trials=args.trials)
        print(evalmod.summary(res))
        # Emit CSV-like data for plotting
        print("workload,baseline_p95,tuned_p95")
        for r in res:
            print(f"{r.workload},{r.baseline_p95:.2f},{r.tuned_p95:.2f}")

if __name__ == "__main__":
    main()
