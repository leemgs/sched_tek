// File: benchmarks/latency_harness.c
// Micro-benchmark to simulate a latency-sensitive, interactive task (e.g., game frame rendering).

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>

#define FRAME_TIME_NS 16666666 // Target 60 FPS

static long long measure_frame_latency()
{
    struct timespec start, end;
    long long elapsed_ns;

    clock_gettime(CLOCK_MONOTONIC, &start);

    // Simulate short CPU burst (interactive work)
    volatile int i;
    for (i = 0; i < 50000; i++) {} 

    // Simulate I/O or sleep (yield the CPU)
    nanosleep((const struct timespec[]){{0, FRAME_TIME_NS / 2}}, NULL);
    
    clock_gettime(CLOCK_MONOTONIC, &end);

    elapsed_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);
    return elapsed_ns;
}

int main(int argc, char *argv[])
{
    int i, num_frames = 1000;
    long long total_latency = 0;
    
    // Simple argument parsing to match the paper's harness concept
    if (argc > 1 && strcmp(argv[1], "--duration") == 0) {
        // In a real harness, we'd parse the duration.
        printf("Running latency harness for specified duration...\n");
    }
    
    FILE *log_file = stdout;
    
    fprintf(log_file, "frame_id,latency_ns\n");

    for (i = 0; i < num_frames; i++) {
        long long latency = measure_frame_latency();
        total_latency += latency;
        fprintf(log_file, "%d,%lld\n", i, latency);
    }

    printf("Harness finished. Average frame latency: %.3f ms\n", (double)total_latency / num_frames / 1e6);

    return 0;
}