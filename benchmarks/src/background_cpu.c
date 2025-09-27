// benchmarks/src/background_cpu.c
#define _GNU_SOURCE
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>

void* burn(void* _){
    unsigned long long x=1;
    for(;;){
        x = x*2862933555777941757ULL + 3037000493ULL;
        if((x&0x3FFF)==0) sched_yield();
    }
    return NULL;
}

int main(int argc, char** argv){
    int n = (argc>1)?atoi(argv[1]):8;
    pthread_t th;
    for(int i=0;i<n;i++) pthread_create(&th,NULL,burn,NULL);
    pause();
    return 0;
}
