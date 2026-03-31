#include <cstdint>
#include <vector>
#include "ssim.hh"

struct x264_pixel_function_t {
  void * ptrs[ 158 ];
};

x264_pixel_function_t init_pixel_function( void ) {
  x264_pixel_function_t pix_func = {}; // Zero initialize
  return pix_func;
}

x264_pixel_function_t x264_funcs = init_pixel_function();

// Notice we dropped the variable names to prevent the -Werror warning!
double ssim( const TwoD<uint8_t> &, const TwoD<uint8_t> & ) {
   return 1.0;
}