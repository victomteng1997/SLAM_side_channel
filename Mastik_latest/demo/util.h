#ifndef _UTIL_H
#define _UTIL_H

static inline int memaccess(void *v) {
  int rv;
  asm volatile("mov (%1), %0": "+r" (rv): "r" (v):);
  return rv;
}

static inline uint32_t memaccesstime(void *v) {
  uint32_t rv;
  asm volatile (
      "mfence\n"
      "lfence\n"
      "rdtscp\n"
      "mov %%eax, %%esi\n"
      "mov (%1), %%eax\n"
      "rdtscp\n"
      "sub %%esi, %%eax\n"
      : "=&a" (rv): "r" (v): "ecx", "edx", "esi");
  return rv;
}

static inline void clflush(void *v) {
  asm volatile ("clflush 0(%0)": : "r" (v):);
}

static inline uint32_t rdtscp() {
  uint32_t rv;
  asm volatile ("rdtscp": "=a" (rv) :: "edx", "ecx");
  return rv;
}

static inline uint64_t rdtscp64() {
  uint32_t low, high;
  asm volatile ("rdtscp": "=a" (low), "=d" (high) :: "ecx");
  return (((uint64_t)high) << 32) | low;
}

static inline void mfence() {
  asm volatile("mfence");
}

static inline int slotwait(uint64_t slotend) {
  if (rdtscp64() > slotend)
    return 1;
  while (rdtscp64() < slotend)
    ;
  return 0;
}

#endif