// benchmarks/src/interactive_sim.c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>
#include <unistd.h>
#include <sched.h>

static inline long nsec_diff(struct timespec a, struct timespec b){
    return (a.tv_sec-b.tv_sec)*1000000000L + (a.tv_nsec-b.tv_nsec);
}

volatile int token = 0;
pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t  cv = PTHREAD_COND_INITIALIZER;

void* worker(void* _){
    cpu_set_t cs; CPU_ZERO(&cs); CPU_SET(0, &cs);
    pthread_setaffinity_np(pthread_self(), sizeof(cs), &cs);
    for(;;){
        pthread_mutex_lock(&mu);
        while(!token) pthread_cond_wait(&cv, &mu);
        token = 0;
        pthread_mutex_unlock(&mu);
        for (volatile int i=0;i<15000;i++); // tiny work
    }
    return NULL;
}

int main(int argc, char** argv){
    int reps = (argc>1)?atoi(argv[1]):2000;
    const char* out = (argc>2)?argv[2]:"../results/interactive_latency.csv";
    FILE* f = fopen(out,"w"); if(!f){perror("fopen"); return 1;}
    fprintf(f,"iter,ns_delay\n");

    pthread_t th; pthread_create(&th,NULL,worker,NULL);

    struct timespec t0,t1;
    for(int i=0;i<reps;i++){
        clock_gettime(CLOCK_MONOTONIC,&t0);
        pthread_mutex_lock(&mu);
        token = 1;
        pthread_cond_signal(&cv);
        pthread_mutex_unlock(&mu);
        sched_yield();
        clock_gettime(CLOCK_MONOTONIC,&t1);
        fprintf(f,"%d,%ld\n",i,nsec_diff(t1,t0));
        usleep(1000);
    }
    fclose(f);
    return 0;
}
