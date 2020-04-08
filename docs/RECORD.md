# Recording Assignments with `stograde record`

In broad strokes, `stograde record` does the following:

- Given a folder name, it `cd`'s into that folder for each student
- It prints the contents of each file
- It tries to compile those files, and records any warnings and errors
- It runs any tests on those files, and records the output.
It can also pass input to stdin during the execution.

`record`'s logs are spit out into the `logs` folder in the current directory.

You'll want to make sure that you have everything needed for testing installed on your machine.
This may include g++, libcurl, etc. depending on the course.

### In More Detail
`record`'s actions are controlled by the specs in the `data/specs` directory.
For a detailed explanation of specs, see SPECS.md.

```yaml
---
assignment: hw2

compilers:
  - &cpp 'g++ --std=c++11 $@ -o $@.exec'

files:
  - file: types.cpp
    commands: *cpp
    tests: $@.exec
```

This spec will go into the `hw2` folder and look for the `types.cpp` file.
If it's not found, it'll print a warning to the log, and exit.
See the SPECS.md documentation for more details.

If it exists, it's compiled with the `cpp` compiler command, as listed under `compilers`.
The syntax for variables takes after `make` a bit here; `$@` is the "target" of the command, so it'll compile `types.cpp` into `types.cpp.exec`.

Once every file has been compiled, the tests are run.
In this case, all that happens is that the binary is called.
The output is caught and redirected to the log file.
This is repeated for every test.

After the tests are complete, the toolkit removes any artifacts and resets the repository to the state of the last commit.

The toolkit then spits out the log into `logs/log-$ASSIGNMENT.md`, which will look something like this:

```markdown
# hw2 – rives
First submission for HW2: 2/11/17 17:00:44

Repository has unmerged branches:
  - remotes/origin/lab8


## types.cpp (Thu Feb 11 17:00:44 2016 -0600)
    ```cpp
    #include <iostream>
    #include <string>
    using namespace std;

    signed int a;
    unsigned int b;
    signed short int c;
    unsigned short int d;
    signed long int e;
    unsigned long int f;
    float g;
    double i;
    long double k;
    char name;
    wchar_t names;
    bool statement;
    signed char money;
    unsigned char ages;

    int main()
    {
      b = -50;
      cout << b << endl; //prints 4294967246

      //c = 5000000000000;
      //cout << c << endl;   //Overflow error in short int

      return 0;
    }
    ```


**no warnings: `g++ --std=c++11 ./types.cpp -o ./types.cpp.exec`**


**results of `./types.cpp.exec`** (status: success)
    ```
    4294967246
    ```
```

Then, you can just scroll through the file, seeing what people submitted, and saving you from needing to `cd` between every folder and make each part of the assignment manually.

### Advanced Usage
`--course {sd|hd|ads|os}` affects the calculation of the base Stogit URL.
If not specified explicitly, this will be inferred based on which specs are downloaded. 

`--stogit URL` lets you force the base url where the repositories are cloned from.
It's passed to `git` in the form `git clone --quiet $URL/$USERNAME.git`.

`--gist` creates a private gist instead of a log file.
*If you don't use this argument, no data ever leaves your system.*

`--date GIT_DATE` checks out the repositories as of GIT\_DATE, and runs everything based on that state.
Powerful, but not used much.
(Theoretically, you could grade everyone's submissions as to their timeliness after the semester is over with this, but that's a bad idea.)
See `man git-rev-parse` for more information on what a GIT\_DATE is.

`--workers` controls the amount of parallelization.
It defaults to the number of logical processors in your machine.
`-w1` will disable the process pool entirely, which is helpful for debugging.

For other options, run `stograde record -h`.
