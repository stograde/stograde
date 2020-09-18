#include"../show_mem.h"  // change the include

int main() {
  init();  // get ready to visualize memory

  short s = 6502;
  char c1 = 106, c2 = 111;
  unsigned int n = 1000000;
  long m = 1000000000000L;
  double d = 3.1415926532389;
  float f = 5.2;

  put_short_at(0, s);  // place the bytes of s at position 0
  put_char_at(2, c1);  // similarly, place c1 at position 2
  put_char_at(3, c2);
  put_unsigned_int_at(4, n);
  put_long_at(8, m);
  put_double_at(16, d);
  put_float_at(24, f);

  quit();  // send memory to the browser for display and clean up
}
