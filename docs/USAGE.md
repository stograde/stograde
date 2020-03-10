# Usage

This toolkit can do a bunch of things, including

- simply manage a set of student repositories
- check which assignments the students have turned in
- run tests against those assignments and produce a log file
- checking out the contents of a student's submission at a given date/time
- viewing programs one at a time in the SD_app React app

## Manage Repositories

If you only want to manage the repositories, all you need to do is 

- put your list of students into `students.txt`
- run `stograde --quiet`.

It will clone the repositories into `students/$USERNAME` and exit.
(`--quiet` just disables the printing of the summary table.)

## Summary Chart

When running the toolkit, a chart is printed out at the end to give you an overview of what has been turned in.
You can just run `stograde` to produce something like this:

```
USER       | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 5 6 7 8 9 10 11 | 1 2
–––––––––––+–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+––––––––––––––––––––––––-|-----
rives      | 1 2 3 4 5 6 7 8 9 10 11 12 13 –– 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11 | 1 - 
student1   | 1 2 3 4 5 6 7 8 9 10 11 12 13 –– –– –– 17 18 19 –– –– –– –– –– –– | 1 2 – 4 – 6 7 – – –– –– | - - 
magnusow   | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – – 7 8 9 10 11 | 1 2 
volz       | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11 | 1 2 
piersonv   | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11 | - 2
```

The first set of columns are the homeworks, the second are the labs, and the third are the worksheets.

### Options

You can use the `--section`, `--my`, `--all`, and `--students` arguments to filter which students are processed.

- `--section` relies on there being sections in the `students.txt` file
- `--my` is shorthand for `--section my`
- `--all` is a superset of all sections
- `--students` overrides all of the other options.
For example, `--students rives piersonv` would only look at those two students.

You can use the `--sort-by` argument to sort the table, as well.
`name` is the default, sorting by username.
`count` sorts by the number of completed submissions.

If you want the table as quickly as possible, pass `-n`/`--no-check` to bypass the remote repository check.

`--partials` can be passed to highlight any partial submissions.

## Recording Submissions for Grading

The toolkit also takes a `--record` parameter.
In broad strokes, `--record` does the following:

- Given a folder name, it `cd`'s into that folder for each student
- It prints the contents of each file
- It tries to compile those files, and records any warnings and errors
- It runs any tests on those files, and records the output.
It can also pass input to stdin during the execution.

`--record`'s logs are spit out into the `logs` folder in the current directory.

You'll want to make sure that you have everything needed for testing installed on your machine.
This may include g++, libcurl, etc. depending on the course.

### In More Detail
`--record`'s actions are controlled by the [homework specs](https://github.com/stodevx/cs251-specs) in the `data/specs`
folder.

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


**no warnings: `g++ --std=c++11 ./types.cpp -o ./types.cpp.exec`**


**results of `./types.cpp.exec`** (status: success)

    4294967246
```

Then, you can just scroll through the file, seeing what people submitted, and saving you from needing to `cd` between every folder and make each part of the assignment manually.

### Advanced Usage
`--course {sd|hd|ads|os}` affects the calculation of the base Stogit URL, allowing you to use the toolkit for other courses.

`--stogit URL` lets you force the base url where the repositories are cloned from.
It's passed to `git` in the form `git clone --quiet $URL/$USERNAME.git`.

`--gist` creates a private gist so you can see the nice syntax highlighting.
*If you don't use this argument, no data ever leaves your system.*

`--clean` removes the student folders and re-clones them, the same as `rm -rf ./students` would.

`--date GIT_DATE` checks out the repositories as of GIT\_DATE, and runs everything based on that state.
Powerful, but not used much.
(Theoretically, you could grade everyone's submissions as to their timeliness after the semester is over with this, but that's a bad idea.)
See `man git-rev-parse` for more information on what a GIT\_DATE is.

`--workers` controls the amount of parallelization.
It defaults to the number of cores in your machine.
`-w1` will disable the process pool entirely, which is helpful for debugging.

`--web` starts a web server to view programs created for the SD_app React app

## Web File Command Line Interface

Files created for the SD React App need to be graded differently.
They need the browser React app to view how they render.
This poses an issue, as the toolkit was originally designed for homeworks that only use the command line.
A command line interface was designed that allows you to view students' files in the app.

### Starting the CLI

The CLI requires three flags:
- `--record HW` - telling the toolkit which homework to grade for
- `--web` - indicating that you want to use the web CLI
- `--port PORT` - setting the port that the server uses to communicate with the app.
This port is different for each React app user, so you can figure it out by opening the app and looking at the network logs.
The IP it is connecting to will be listed, along with a `:` and a number.
That last number is your port.  

A web server like the `~/bridge.py` used by students is started in a separate thread.
Then a command line interface is started that allows you to choose what file to render.

### Using the CLI

The interface starts with a list of students to choose from:

```
? Choose student  (Use arrow keys)
   QUIT
   LOG and QUIT
   rives
   student1
   magnusow
   volz
   piersonv
   narvae1
``` 

Select a student using the arrow keys and enter.
This will show a `Processing...` message, then show you a list of all files in the homework.

```
? Choose student  narvae1
Processing...
? Choose file  (Use arrow keys)
   BACK
   story.cpp
   weather.cpp
   weather2.cpp
```

Select the file using the arrow keys and enter.
This will compile it and put it in the ./server directory for the server to send to the app.

