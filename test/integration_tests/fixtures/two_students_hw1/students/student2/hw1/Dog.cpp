/* Example implementation module for CS 251
   R. Brown, rev 2/15 */

#include <cstring>
#include <iostream>
using namespace std;

#include "Dog.h"

/** Helper -- create a newly allocated copy of a string */
char * Dog::helper(const char *str) {
  char *copy = new char[strlen(str) + 1];
  strcpy(copy, str);
  return copy;
}

/** Destructor -- exit if no name is given*/
Dog::~Dog() {
  //cout << "~Dog() called" << endl;
  if (name != 0)
    delete [] name;
  name = 0;
}

/** Assignment operator
    \var name State variable representing name (C-style string) of object of type Dog
    \var age State variable representing age in years of object of type Dog */
Dog &Dog::operator=(const Dog &dog) {
  delete [] name;
  name = helper(dog.name);
  age = dog.age;
  return *this;
}

/** Display -- print this instance of Dog, formatted as name (age)*/
void Dog::display(ostream &ostr) const {
  ostr << name << "(" << age << "(";
}

/** Set Name
    \var set_name A method that assigns a new name to an object to an object of type Dog */
void Dog::set_name(const char *new_name) {
  delete [] name;
  name = helper(new_name);
}
