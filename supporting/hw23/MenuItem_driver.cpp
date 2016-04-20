/* driver program for MenuItem.
 RAB rev 10/2014 */

#include <iostream>
using namespace std;


#include "MenuItem.h"

/* helper function for checking state changes from methods
   prints four labelled values of type MenuItem.
   Example call:
     print_all("var1", var1, "var2", var2,
               "var3", var3, "var4", var4)
 */

void print_all
(const char *varname1, const MenuItem &obj1,
 const char *varname2, const MenuItem &obj2,
 const char *varname3, const MenuItem &obj3,
 const char *varname4, const MenuItem &obj4)
{
  cout << "\t" << varname1 << ":\t";
  obj1.display(cout);  cout << endl;
  cout << "\t" << varname2 << ":\t";
  obj2.display(cout);  cout << endl;
  cout << "\t" << varname3 << ":\t";
  obj3.display(cout);  cout << endl;
  cout << "\t" << varname4 << ":\t";
  obj4.display(cout);  cout << endl << endl;
}


/* main() for driver */

int main()
{
  cout << "*** Driver program for MenuItem class ***" << endl;


  cout << endl
       << "*** Testing constructors, assignment operator, display() method ***"
       << endl << endl;


  cout << endl << "Test of typical constructor:" << endl;
  cout << "  MenuItem mi1(10, \"First choice\");" << endl;
  MenuItem mi1(10, "First choice");
  cout << "  calling mi1.display(cout);" << endl
       << "    output is:" << endl;
  mi1.display(cout);   cout << endl;

  cout << endl << "Test of default constructor:" << endl;
  cout << "  MenuItem mi2;" << endl;
  MenuItem mi2;
  cout << "  calling mi2.display(cout);" << endl
       << "    output is:" << endl;
  mi2.display(cout);   cout << endl;

  cout << endl << "Test of copy constructor:" << endl;
  cout << "  MenuItem mi3(mi1);" << endl;
  MenuItem mi3(mi1);
  cout << "  calling mi3.display(cout);" << endl
       << "    output is:" << endl;
  mi3.display(cout);   cout << endl;

  cout << endl << "Test of assignment operator:" << endl;
  cout << "  MenuItem mi4(20, \"Second choice\");" << endl;
  MenuItem mi4(20, "Second choice");
  print_all("mi1", mi1, "mi2", mi2, "mi3", mi3, "mi4", mi4);
  cout << "  calling (mi1 = mi4).display(cout);" << endl
       << "    output is:" << endl;
  (mi1 = mi4).display(cout);   cout << endl;
  cout << "  state change:" << endl;
  print_all("mi1", mi1, "mi2", mi2, "mi3", mi3, "mi4", mi4);
  cout << "  further test of return value from assignment:" << endl;
  cout << "  (mi4 = mi3).set_val(111);" << endl;
  (mi4 = mi3).set_val(111);
  cout << "  state change:" << endl;
  print_all("mi1", mi1, "mi2", mi2, "mi3", mi3, "mi4", mi4);

  cout << endl
       << "*** Testing remaining methods ***"
       << endl << endl;


  cout << endl << "Test of get_ methods:" << endl;
  cout << "  calling mi1.display(cout);" << endl
       << "    output is:" << endl;
  mi1.display(cout);   cout << endl;
  cout << "  mi1.get_label() returns "
       << mi1.get_label() << "." << endl;
  cout << "  mi1.get_val() returns "
       << mi1.get_val() << "." << endl;

  cout << endl << "Test of set_ methods:" << endl;
  cout << "  initial values of all variables:" << endl;
  print_all("mi1", mi1, "mi2", mi2, "mi3", mi3, "mi4", mi4);
  cout << "  mi3.set_label(\"Another choice\");" << endl;
  mi3.set_label("Another choice");
  cout << "  calling mi3.display(cout);" << endl
       << "    output is:" << endl;
  mi3.display(cout);   cout << endl;
  cout << "  mi1.set_val(15);" << endl;
  mi1.set_val(15);
  cout << "  calling mi1.display(cout);" << endl
       << "    output is:" << endl;
  mi1.display(cout);   cout << endl;
  cout << "final values of all variables:" << endl;
print_all("mi1", mi1, "mi2", mi2, "mi3", mi3, "mi4", mi4);
  cout << endl;

  return 0;
}
