/* Example program for CS 251
   R. Brown, rev 2/15 */

#include <iostream>
using namespace std;

#include "Dog.h"


/** Main program */

int main() {
  Dog mydog("Bob", 4);

  cout << "Hello, world!" << endl;
  cout << "My dog is named " << mydog.get_name()
       << ", and it is " << mydog.get_age() << " years old." << endl;

  return 0; /* indicates successful run of the program */
}
