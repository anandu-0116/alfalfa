/* -*-mode:c++; tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2 -*- */

/* Based on (and linked with) libx264 (GPL-2+) */

/* Copyright (C) 2015-2018 the Alfalfa authors

   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License
   as published by the Free Software Foundation; either version 2
   of the License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
   02110-1301, USA. */

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

double ssim( const TwoD<uint8_t> &, const TwoD<uint8_t> & ) {
   return 1.0;
}