/* Example interface module for CS 251
   R. Brown, rev 2/15 */

#ifndef _DOG_H_
#define _DOG_H_

#include <iostream>
using std::ostream;

/** "Dog" class
    \var new_name Name generated for the object of type Dog
    \fn set_name A method that returns name of an object of type Dog
    @param new_name Name for object of type Dog
    \fn birthday A method that adds 1 to the age of an object of type Dog */

class Dog {
protected:
  char *name;
  int age;

public:
  Dog(const char *n, int a) { age = a; name = helper(n); }
  Dog() { age = 0; name = helper(""); }
  Dog(const Dog &dog) { age = dog.age; name = helper(dog.name); }

  ~Dog();

  Dog &operator=(const Dog &dog);
  void display(ostream &ostr) const;

  const char *get_name(void) const { return name; }
  int get_age(void) const { return age; }

  void set_name(const char *new_name);
  void birthday(void) { age++; }

protected:
  char *helper(const char *s); /* helper function */
};

#endif /* _DOG_H_ */
