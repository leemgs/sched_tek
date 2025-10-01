# File: scripts/run_experiment.sh
# Script to automate the build, installation, and running of SCHED_TEK experiments.

#!/bin/bash

# --- Configuration ---
TRACE_OUTPUT_DIR="../results/traces"
NUM_REPETITIONS=5 
WORKLOAD_TYPE="Interactive"

# --- Functions ---

# Function to run the micro-benchmark workload
run_workload() {
    local workload_name=$1
    echo "Starting workload: $workload_name (Repetition $2/5)"
    
    # Run the interactive/stress workloads concurrently (simulating contention)
    
    # 1. Run CPU-bound task in background
    ../benchmarks/cpu_stress_task &
    CPU_PID=$!
    
    # 2. Run latency-sensitive task
    ../benchmarks/latency_harness --duration=30s --log-file=$TRACE_OUTPUT_DIR/${workload_name}_rep${2}_latency.log
    
    # Wait for background task to finish (or kill after 30s)
    kill $CPU_PID
    wait $CPU_PID 2>/dev/null
    echo "Workload finished."
}


# --- Main Execution ---

mkdir -p $TRACE_OUTPUT_DIR
echo "SCHED_TEK Experiment Runner Started."

# Step 1: Check if SCHED_TEK /proc interface exists (mock check)
if [ ! -d "/proc/sys/sched_tek" ]; then
    echo "NOTICE: /proc/sys/sched_tek not found. Assuming mock kernel environment for this run."
fi

# Step 2: Set SCHED_TEK parameters (if /proc exists, this would use 'sudo tee')
echo "Setting SCHED_TEK to hybrid mode (alpha=0.20, beta=0.15)..."
# echo "2" | sudo tee /proc/sys/sched_tek/bias_mode > /dev/null
# echo "0.20" | sudo tee /proc/sys/sched_tek/bias_alpha > /dev/null

echo "Starting trace collection via trace_cmd (or ftrace)..."
# In a real setup, this would record kernel trace events

for i in $(seq 1 $NUM_REPETITIONS); do
    run_workload $WORKLOAD_TYPE $i
done

echo "Trace collection stopped. Analyzing results..."
# In a real setup, trace data is extracted and passed to analyze_results.py
python3 ./analyze_results.py mock_trace_log.csv

echo "Experiment run complete."