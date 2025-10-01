
SCHED\_TEK 패치 시리즈의 최종 구성을 반영하여 `README.md` 파일을 업데이트해 드리겠습니다.

새로운 `README.md`는 재현 아티팩트의 **커널 패치 섹션**에 방금 확정된 8개의 패치 파일을 명확하게 나열하여, 사용자가 패치 적용 순서를 쉽게 이해하고 재현할 수 있도록 돕습니다.

-----

# 📄 업데이트된 `README.md` 파일

```markdown
# SCHED_TEK: Controlled Bias를 활용한 커널 스케줄링 재검토

**SCHED_TEK**은 응답성(responsiveness)과 공정성(fairness)을 함께 최적화하도록 설계된 Linux 커널 스케줄러 수정(패치) 세트입니다. 기존 스케줄러(CFS 등)가 이 두 목표를 상충 관계로 간주하는 것과 달리, SCHED_TEK은 커널 스케줄링 경로에 '제한된 편향(bounded bias)'을 통합하고 부하에 따라 동적으로 조정하여 낮은 꼬리 대기 시간(tail latency)과 높은 처리량을 동시에 달성합니다.

이 저장소는 논문 "Responsiveness Is Not a Trade-Off: Revisiting Kernel Scheduling with Controlled Bias"의 재현 아티팩트입니다.

## 주요 기능

1.  **Vruntime 편향 엔진 (Vruntime Biasing):** 대화형(interactive) 태스크를 선호하기 위해 가상 실행 시간(**vruntime**) 업데이트에 비선형 스케일링 항을 도입합니다.
    * **핵심 공식:** `vruntime = vruntime + Δt * (1 + α * B_i)`
2.  **하이브리드 제어기 (Hybrid Controller):** **Jain의 지수(Jain's index)**와 **기아(starvation) 발생률**을 모니터링하여 편향 계수 `α`와 `β`를 동적으로 조정합니다. 이 피드백 루프는 부하가 높을 때 공정성 저하를 방지합니다.
3.  **/proc 제어 인터페이스:** `bias_alpha`, `bias_beta`, `bias_mode`와 같은 매개변수를 런타임에 안전하게 조정할 수 있는 최소한의 제어 표면을 제공합니다.

## 재현 아티팩트 구성

본 아티팩트는 **Linux Kernel 6.8+** 버전을 대상으로 합니다.

```

sched\_tek\_artifact/
├── kernel\_patches/          \# SCHED\_TEK의 핵심 로직을 포함하는 커널 패치 파일 (C/C++ 유사 코드)
├── benchmarks/              \# 성능 및 공정성 평가에 사용된 부하 생성기 및 하니스 (C 코드)
├── scripts/                 \# 커널 빌드/설치, 실험 실행, 결과 분석을 위한 스크립트 (Python/Shell)
├── LICENSE.md               \# Apache-2.0 라이선스
└── README.md

````

## 🛠️ SCHED\_TEK 커널 패치 시리즈 (8/8)

다음은 Linux 커널 소스 트리에 순서대로 적용되어야 하는 8개의 패치 파일입니다.

| 파일 번호 | 파일명 | 주요 역할 |
| :--- | :--- | :--- |
| **0000** | `0000-sched-Enable-SCHED_TEK-build-and-Kconfig.patch` | 빌드 시스템 설정 및 SCHED\_TEK 활성화 |
| **0001** | `0001-sched-Introduce-SCHED_TEK-framework.patch` | 기본 데이터 구조 및 초기화 프레임워크 도입 |
| **0002** | `0002-sched-tek-Implement-vruntime-biasing.patch` | **핵심 기능:** vruntime 편향 엔진 구현 |
| **0003** | `0003-sched-tek-Add-hybrid-controller-and-proc-interface.patch` | **핵심 기능:** 동적 제어기 및 태스크 선택 로직 |
| **0004** | `0004-sched-tek-Add-mitigations-and-security-guardrails.patch` | 안정성 및 보안 완화(Mitigations) 로직 추가 |
| **0005** | `0005-sched-tek-Add-NUMA-awareness-and-load-distribution.patch` | NUMA 아키텍처 인지 및 부하 분산 최적화 |
| **0006** | `0006-sched-tek-Add-tracing-and-debug-interfaces.patch` | 성능 모니터링을 위한 트레이싱 및 디버그 훅 추가 |
| **0007** | `0007-sched-tek-Add-official-documentation.patch` | SCHED\_TEK 커널 공식 문서화 |
| **0008** | `0008-sched-tek-Final-cleanup-and-series-submission-note.patch` | 최종 정리 및 패치 시리즈 완료 |

## 재현 단계 (Step-by-Step Reproduction)

1.  **환경 설정:** Linux Kernel 6.8 이상 버전이 설치된 x86_64 또는 ARM big.LITTLE 시스템을 준비합니다. `gcc 12.2+`, `make`, `python3` (numpy, pandas 포함)가 필요합니다.
2.  **커널 패치 적용:**
    ```bash
    cd <LINUX_KERNEL_SOURCE>
    # 8개 패치를 순서대로 적용
    patch -p1 < path/to/sched_tek_artifact/kernel_patches/000*.patch
    ```
3.  **커널 빌드 및 설치:** 패치된 커널을 빌드하고 부팅합니다.
4.  **실험 실행:**
    ```bash
    cd scripts/
    ./run_experiment.sh
    ```
5.  **결과 분석:** `scripts/analyze_results.py`를 사용하여 수집된 로그(trace_cmd 등)를 처리하고 P95 대기 시간, Jain의 지수, Perf/W 등의 최종 수치를 계산합니다.

## 설정 매개변수 (Defaults & Safe Ranges)

| 매개변수 | 기본값 | 안전 범위 | 설명 |
| :--- | :--- | :--- | :--- |
| \`bias_alpha\` | 0.20 | [0.10, 0.35] | Vruntime 편향 계수 (\`α\`) |
| \`bias_beta\` | 0.15 | [0.05, 0.30] | 런큐 선택 증폭 계수 (\`β\`) |
| \`bias_mode\` | hybrid | {static, adaptive, hybrid} | 제어기 모드 |

## 라이선스

이 프로젝트는 **Apache-2.0** 라이선스를 따릅니다. 자세한 내용은 \`LICENSE.md\`를 참조하십시오.
````
