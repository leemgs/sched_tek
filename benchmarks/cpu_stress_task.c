// File: benchmarks/cpu_stress_task.c
// Simple CPU-bound task to generate high contention, simulating a background batch job.

#include <stdio.h>
#include <time.h>

#define RUN_DURATION_S 60

int main()
{
    time_t start_time = time(NULL);
    time_t current_time;
    double result = 1.0;
    long long count = 0;
    
    printf("Starting CPU stress task...\n");
    
    // Run for a duration
    do {
        // Heavy computation loop
        for (int i = 0; i < 1000000; i++) {
            result *= 1.000000001; 
            if (result > 2.0) result = 1.0;
        }
        count++;
        current_time = time(NULL);
    } while ((current_time - start_time) < RUN_DURATION_S);

    printf("CPU stress task finished after %ld seconds. Total iterations: %lld\n", current_time - start_time, count);
    
    return 0;
}