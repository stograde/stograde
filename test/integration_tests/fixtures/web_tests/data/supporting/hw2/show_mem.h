#ifndef _SHOW_MEM_H_
#define _SHOW_MEM_H_

// these functions must be used at the start and end of main()
void init(bool _use_cache = false);
void quit(const char *c = 0);

// these functions place a new variable at a given index
bool &bool_at(int index, bool shared=false);
char &char_at(int index, bool shared=false);
unsigned char &uchar_at(int index, bool shared=false);
short &short_at(int index, bool shared=false);
unsigned short &unsigned_short_at(int index, bool shared=false);
int &int_at(int index, bool shared=false);
unsigned int &unsigned_int_at(int index, bool shared=false);
long &long_at(int index, bool shared=false);
long long &long_long_at(int index, bool shared=false);
float &float_at(int index, bool shared=false);
double &double_at(int index, bool shared=false);

// new functions for obtaining and writing data into global_mem
bool get_bool_at(int index, bool shared=false);
char get_char_at(int index, bool shared=false);
unsigned char get_uchar_at(int index, bool shared=false);
short get_short_at(int index, bool shared=false);
unsigned short get_unsigned_short_at(int index, bool shared=false);
int get_int_at(int index, bool shared=false);
unsigned int get_unsigned_int_at(int index, bool shared=false);
long get_long_at(int index, bool shared=false);
long long get_long_long_at(int index, bool shared=false);
float get_float_at(int index, bool shared=false);
double get_double_at(int index, bool shared=false);

void put_bool_at(int index, bool val, bool shared=false);
void put_char_at(int index, char val, bool shared=false);
void put_uchar_at(int index, unsigned char val, bool shared=false);
void put_short_at(int index, short val, bool shared=false);
void put_unsigned_short_at(int index, unsigned short val, bool shared=false);
void put_int_at(int index, int val, bool shared=false);
void put_unsigned_int_at(int index, unsigned int val, bool shared=false);
void put_long_at(int index, long val, bool shared=false);
void put_long_long_at(int index, long long val, bool shared=false);
void put_float_at(int index, float val, bool shared=false);
void put_double_at(int index, double val, bool shared=false);

// this function requires fetch.o -lcurl when compiling
void fetch(const char *url, int index = 0, int len = -1);

// these functions assume ppm format images
void read_image(const char *filename);
void get_image_dimensions(int &width, int &height);
void set_image_dimensions(int width, int height);
void write_image(const char *filename);

#endif // _SHOW_MEM_H_
