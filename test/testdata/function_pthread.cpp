#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <print>

constexpr int LOOP_COUNT = 100000000;

void* ChildThreadFunction(void*) {
  for (volatile int i = 0; i < LOOP_COUNT; i += 1) {
  }
  return nullptr;
}

void MainThreadFunction() {
  for (volatile int i = 0; i < LOOP_COUNT; i += 1) {
  }
}

int main() {
  while (true) {
    pthread_t thread;
    int ret = pthread_create(&thread, nullptr, ChildThreadFunction, nullptr);
    if (ret != 0) {
      std::println(stderr, "pthread_create failed: {}", strerror(ret));
      exit(1);
    }
    MainThreadFunction();
    ret = pthread_join(thread, nullptr);
    if (ret != 0) {
      std::println(stderr, "pthread_join failed: {}", strerror(ret));
      exit(1);
    }
  }
  return 0;
}
