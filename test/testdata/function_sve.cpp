#ifdef __ARM_FEATURE_SVE
#include <arm_sve.h>
#include <sys/auxv.h>
#include <array>
#include <cstddef>

void vector_multiply_sve(const float* a, const float* b, float* res, size_t n) {
  size_t i = 0;
  // Create a predicate for 32-bit floats (svbool_t)
  svbool_t pg = svwhilelt_b32(i, n);

  // Loop while the predicate has active lanes
  while (svptest_any(svptrue_b32(), pg)) {
    // Load vectors from a and b
    svfloat32_t va = svld1_f32(pg, &a[i]);
    svfloat32_t vb = svld1_f32(pg, &b[i]);

    // Multiply: res = va * vb
    svfloat32_t vres = svmul_f32_x(pg, va, vb);

    // Store result
    svst1_f32(pg, &res[i], vres);

    // Increment index by vector length
    i += svcntw();
    // Update predicate for next iteration
    pg = svwhilelt_b32(i, n);
  }
}

void fill_random_sve(float* array, size_t n, float seed) {
  size_t i = 0;

  // svwhilelt creates a mask: "While index 'i' is less than 'n'"
  svbool_t pg = svwhilelt_b32(i, n);

  while (svptest_any(svptrue_b32(), pg)) {
    // 1. Generate an integer index vector [i, i+1, i+2...] and convert to float
    svint32_t v_index_int = svindex_s32(static_cast<int32_t>(i), 1);
    svfloat32_t v_index = svcvt_f32_s32_z(pg, v_index_int);

    // 2. Perform math on the whole vector at once
    svfloat32_t v_random = svadd_f32_z(pg, v_index, svdup_f32(seed));

    // 3. Store the result into the array
    svst1_f32(pg, &array[i], v_random);

    // 4. Move the index forward by the "vector length"
    i += svcntw();

    // 5. Update the safety sensor for the next batch
    pg = svwhilelt_b32(i, n);
  }
}

inline bool SystemCanUseVgReg() {
  static const bool supported = [] -> bool {
#if defined(__linux__) && defined(__aarch64__)
    const unsigned long hwcaps = getauxval(AT_HWCAP);
    const unsigned long hwcaps2 = getauxval(AT_HWCAP2);
    return (hwcaps & HWCAP_SVE) || (hwcaps2 & HWCAP2_SVE2);
#else
    return false;
#endif
  }();
  return supported;
}

// A helper to prevent the compiler from optimizing away our math
void inline escape(void* p) {
  __asm__ volatile("" : : "g"(p) : "memory");
}

int main() {
  if (!SystemCanUseVgReg()) {
    return 0;
  }

  constexpr size_t array_size = 1024;
  std::array<float, array_size> a;
  std::array<float, array_size> b;
  std::array<float, array_size> result;

  while (true) {
    fill_random_sve(a.data(), a.size(), 42.0f);
    fill_random_sve(b.data(), b.size(), 22.0f);
    vector_multiply_sve(a.data(), b.data(), result.data(), array_size);
    escape(result.data());
  }

  return 0;
}
#else
int main() {
  return 0;
}
#endif
