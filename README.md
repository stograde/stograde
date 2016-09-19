# cs251-toolkit
![pypi version](https://img.shields.io/pypi/v/cs251tk.svg)

Welcome to the CS251 toolkit, designed to help TAs and graders for St. Olaf's Software Design course.

This toolkit can be used to

- simply manage a set of student repositories (`cs251tk`)
- check which assignments the students have turned in (`cs251tk`)
- run tests against those assignments and produce a log file (`cs251tk --record hw3`)

See the ["Run the thing"](#run-the-thing) section for details.

## Getting Started

Prerequisites: macOS/Linux, Python 3.4+, git.

##### Make the folder
```console
mkdir cs251/
cd cs251
pyvenv ./venv
source ./venv/bin/activate  # or activate.csh
# deactivate  # will exit the venv
```

This will set up a "virtual environment" for python, just for this folder, so that any dependencies we use here don't overwrite the system.  Also we don't get system-level access to install things, so this just makes it all easier.

The _only_ tricky thing is that you have to remember to run `source ./venv/bin/activate` whenever you get into this folder, or else you won't be able to run the toolkit. (why virtualenvs? read [virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and [pip-virtualenv](http://docs.python-guide.org/en/latest/dev/pip-virtualenv).)

> If you really don't want to use the virtualenv, you can substitute the `pip install` for `pip3 install --user` in the next step. You'll also need to add `$HOME/.local/bin` to your `$PATH`. Consult Google or your local unix guru for help.


##### Install the toolkit

```console
pip install cs251tk
```

The toolkit is distributed via `pip`, which is (more or less) Python's packaging system. `pip install` will install something globally, but on the lab machines we don't have global access, so we use the handy virtual environment we created in the last step, instead.


##### Grab the course specs

```console
git clone https://github.com/StoDevX/cs251-specs data
```

The toolkit expects to be run in a folder that contains both a `data` folder and a `students.txt` file. The `data` folder should have a `specs` subfolder, which should have at least a `specs` folder. If any specs need to provide sample input, they should go under a `supporting/hw#` folder that matches the assignment name.

##### List your students

```console
touch students.txt
```

Put a newline-separated list of your students in `./students.txt`.

The students file can also include delimited sections of students, which allows the `--section-a` arguments to work. If no sections are provided, all students are assumed to be in the `[my]` section.

###### Basic Sample

```ini
rives
piersonv
```

###### More Involved Sample

```ini
[my]  # this is a section
rives

[section-a]  # as is this
rives
piersonv

[section-b]  # the comments aren't necessary
magnusow
```

## Run the thing

> Please only run this in your `cs251` folder. I know it makes at least one folder in whatever directory it's run from, so unless you like cluttering up your filesystem with `.cs251toolkitrc.yaml` files, pick a folder and run it in there :wink:.

```console
cs251tk --help
```

As mentioned in the introduction, this toolkit can do a bunch of things, including

- simply manage a set of student repositories
- check which assignments the students have turned in
- run tests against those assignments and produce a log file
- checking out the contents of a student's submission at a given date/time

If you only want to manage the repositories, all you need to do is put your list of students into `students.txt` and run `cs251tk --quiet`. It will clone the repositories into `./students/$USERNAME` and exit. (`--quiet` just disables the printing of the summary table.)

## Summaries

If you want to see the summary table of what people've turned in, you can just run `cs251tk` to produce something like this:

```text
USER       | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 5 6 7 8 9 10 11
–––––––––––+–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+––––––––––––––––––––––––
rives      | 1 2 3 4 5 6 7 8 9 10 11 12 13 –– 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11
student    | 1 2 3 4 5 6 7 8 9 10 11 12 13 –– –– –– 17 18 19 –– –– –– –– –– –– | 1 2 – 4 – 6 7 – – –– ––
magnusow   | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – – 7 8 9 10 11
volz       | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11
piersonv   | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11
```

The first set of columns are the homeworks, and the second are the labs.

You can use the `--section`, `--my`, `--all`, and `--students` arguments to filter which students are processed.

- `--section` relies on there being sections in the `students.txt` file
- `--my` is shorthand for `--section my`
- `--all` is a superset of all sections
- `--students` overrides all of the other options. For example, `--students rives piersonv` would only look at those two students.

You can use the `--sort-by` argument to sort the table, as well. `name` is the default, sorting by username, and `count` sorts by the number of submissions.

If you want the table as quickly as possible, pass `-n`/`--no-check` to bypass the remote repository check.

`--partials` can be passed to highlight any partial submissions.


## Recording Submissions

The toolkit also takes a `--record` parameter. In broad strokes, `--record` does the following:

- given a folder name, it `cd`'s into that folder for each student
- it prints the contents of each cpp file within the folder
- it tries to compile each `.cpp` file, and records any warnings and errors
- it runs each file, and records the output. It can also pass input to stdin during the execution

`--record`'s logs are spit out into the `logs` folder in the current directory.

If you're running this on something other than a lab machine, you'll want to have `gcc` installed.


###### In a bit more detail
`--record`'s actions are controlled by the [homework specs](https://github.com/stodevx/cs251-specs) in the `data/specs` folder.

```yaml
---
assignment: hw2

compilers:
  - &cpp 'g++ --std=c++11 $@ -o $@.exec'

files:
  - [ types.cpp, *cpp ]

tests:
  - [ types.cpp, $@.exec ]
```

This spec will go into the `hw2` folder and look for the `types.cpp` file. If it's not found, it'll print a warning to the log, and exit.

If it exists, it's compiled with the `cpp` compiler command, as listed under `compilers`. The syntax for variables takes after `make` a bit here; `$@` is the "target" of the command, so it'll compile `types.cpp` into `types.cpp.exec`.

Once every file has been compiled, the tests are run. In this case, all that happens is that the binary is called. The output is caught and redirected to the log file. This is repeated for every test.

After the tests are complete, the toolkit removes any artifacts and resets the repository to the state of the last commit.

The toolkit then spits out the log into `logs/log-$ASSIGNMENT.md`, which will look something like this:

```markdown
# hw2 – rives

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


## `cs251tk --help`

```text
usage: cs251tk [-h] [--students USERNAME [USERNAME ...]]
               [--section SECTION [SECTION ...]] [--all] [--quiet]
               [--no-progress] [--workers N] [--sort {name,count}]
               [--partials] [--clean] [--no-update] [--stogit URL]
               [--day {sun,mon,tues,wed,thurs,fri,sat}] [--date YYYY-MM-DD]
               [--no-check] [--record HW [HW ...]] [--gist]
               [input [input ...]]

The core of the CS251 toolkit

positional arguments:
  input                 A mixed list of students and assignments

optional arguments:
  -h, --help            show this help message and exit

student-selection arguments:
  --students USERNAME [USERNAME ...]
                        Only iterate over these students.
  --section SECTION [SECTION ...]
                        Only check these sections: my, all, a, b, etc
  --all, -a             Shorthand for '--section all'

optional arguments:
  --quiet, -q           Don't show the table
  --no-progress         Hide the progress bar
  --workers N, -w N     The number of operations to perform in parallel
  --sort {name,count}   Sort the students table
  --partials, -p        Highlight partial submissions

student management arguments:
  --clean               Remove student folders and re-clone them
  --no-update, -n       Do not update the student folders when checking
  --stogit URL          Use an alternate stogit base URL

time-based arguments:
  --day {sun,mon,tues,wed,thurs,fri,sat}
                        Check out submissions as of 5pm on WEEKDAY
  --date YYYY-MM-DD     Check out submissions as of 5pm on DATE

grading arguments:
  --no-check, -c        Do not check for unmerged branches
  --record HW [HW ...]  Record information on student submissions. Requires a
                        spec file
  --gist                Post overview table and student recordings as a
                        private gist
```


## Advanced Usage
`--stogit URL` lets you change the base url where the repositories are cloned from. It's passed to `git` in the form `git clone --quiet $URL/$USERNAME.git`.

`--gist` creates a private gist so you can see the nice syntax highlighting. If you don't use this argument, no data ever leaves your system.

`--clean` removes the student folders and re-clones them, the same as `rm -rf ./students` would.

`--day` and `--date` have a tendency to break, but _in short_, they check out the repositories as of 5pm on $DATE and run everything based on that state. Powerful, but not used much. (Theoretically, you could grade everyone's submissions as to their timeliness after the semester is over with this, but that's a bad idea.)

`--workers` controls the amount of parallelization. It defaults to the number of cores in your machine. `-w1` will disable the process pool entirely, which is helpful for debugging.


## Contributing
- `git clone https://github.com/StoDevX/cs251-toolkit`
- `cd cs251-toolkit`
- `pyvenv ./venv`
- `source ./venv/bin/activate`
- `python3 setup.py develop`
- go to your cs251 folder that contains the data/ and students/ folders
- run `cs251tk`; it'll be the development version.
- run `deactivate` to leave the venv.


## Maintainers
- You need a PyPI account: [pypi.org](https://pypi.org)
- `python3 setup.py sdist upload` should generate a new release and upload it to PyPI
