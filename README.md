# cs251-toolkit
[![PyPI](https://img.shields.io/pypi/v/cs251tk.svg)](https://pypi.python.org/pypi/cs251tk) [![TraviCI](https://travis-ci.org/StoDevX/cs251-toolkit.svg?branch=master)](https://travis-ci.org/StoDevX/cs251-toolkit) [![Coverage Status](https://coveralls.io/repos/github/StoDevX/cs251-toolkit/badge.svg?branch=master)](https://coveralls.io/github/StoDevX/cs251-toolkit?branch=master)

Welcome to the CS251 toolkit, designed to help TAs and graders for St. Olaf's Software Design course.

This toolkit can be used to

- simply manage a set of student repositories (`cs251tk`)
- check which assignments the students have turned in (`cs251tk`)
- run tests against those assignments and produce a log file (`cs251tk --record hw3`)

See the ["Run the thing"](#run-the-thing) section for details.

## Getting Started

Prerequisites: macOS/Linux/Windows Linux Subsystem, Python 3.5+, git.

##### Make the folder
```console
$ mkdir cs251/
$ cd cs251
```
> For Hardware Design, use `cs241` for your directory name.

You'll need to add either `~/.local/bin` (if you're on Linux) or `~/Library/Python/3.X/bin` (if you're on macOS, where `X` is your python version – check with `python3 -V`) to your `$PATH`. Consult Google or your local unix guru for help.


##### Install the toolkit

```console
$ pip3 install --user cs251tk
```

The toolkit is distributed via `pip`, which is (more or less) Python's packaging system. `pip3 install` will install something globally, but since we don't have global access on the lab machines we'll give it the `--user` flag, which installs into your home folder, instead.

> When you need to update the toolkit, use `pip3 install --user --no-cache --upgrade cs251tk`.


##### Grab the course specs

###### Software Design

```console
$ # make sure you're still in the cs251 folder
$ git clone https://github.com/StoDevX/cs251-specs data
```

###### Hardware Design

```console
$ # make sure you're still in the cs241 folder
$ git clone https://github.com/StoDevX/cs241-specs data
```

The toolkit expects to be run in a folder that contains both a `data` folder and a `students.txt` file. The `data` folder should have a `specs` subfolder, which should have at least a `specs` folder. If any specs need to provide sample input, they should go under a `supporting/hw#` folder that matches the assignment name.

##### List your students

```console
$ touch students.txt
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

```console
$ cs251tk --help
```

As mentioned in the introduction, this toolkit can do a bunch of things, including

- simply manage a set of student repositories
- check which assignments the students have turned in
- run tests against those assignments and produce a log file
- checking out the contents of a student's submission at a given date/time

If you only want to manage the repositories, all you need to do is put your list of students into `students.txt` and run `cs251tk --quiet`. It will clone the repositories into `students/$USERNAME` and exit. (`--quiet` just disables the printing of the summary table.)

## Summaries

If you want to see the summary table of what people've turned in, you can just run `cs251tk` to produce something like this:

```text
USER       | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 5 6 7 8 9 10 11
–––––––––––+–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+––––––––––––––––––––––––
rives      | 1 2 3 4 5 6 7 8 9 10 11 12 13 –– 15 16 17 18 19 20 21 22 23 24 25 | 1 2 3 4 – 6 7 8 9 10 11
student1   | 1 2 3 4 5 6 7 8 9 10 11 12 13 –– –– –– 17 18 19 –– –– –– –– –– –– | 1 2 – 4 – 6 7 – – –– ––
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

You can use the `--sort-by` argument to sort the table, as well. `name` is the default, sorting by username, and `count` sorts by the number of completed submissions.

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


## `cs251tk --help`

```text
usage: cs251tk [-h] [--debug] [--students USERNAME [USERNAME ...]]
               [--section SECTION [SECTION ...]] [--all] [--quiet]
               [--no-progress] [--workers N] [--sort {name,count}]
               [--partials] [--clean] [--no-update] [--stogit URL]
               [--date GIT_DATE] [--no-check] [--record HW [HW ...]] [--gist]
               [input [input ...]]

The core of the CS251 toolkit

positional arguments:
  input                 A mixed list of students and assignments

optional arguments:
  -h, --help            show this help message and exit
  --debug               enable debugging mode (throw errors, implies -w1)

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
  --date GIT_DATE       Check out last submission on DATE (eg, "last week",
                        "tea time", "2 hrs ago") (see `man git-rev-list`)

grading arguments:
  --no-check, -c        Do not check for unmerged branches
  --record HW [HW ...]  Record information on student submissions. Requires a
                        spec file
  --gist                Post overview table and student recordings as a
                        private gist
```


## Advanced Usage
`--course {sd|hd}` affects the calculation of the base Stogit URL, allowing you to use the toolkit for hardware design as well.

`--stogit URL` lets you force the base url where the repositories are cloned from. It's passed to `git` in the form `git clone --quiet $URL/$USERNAME.git`.

`--gist` creates a private gist so you can see the nice syntax highlighting. If you don't use this argument, no data ever leaves your system.

`--clean` removes the student folders and re-clones them, the same as `rm -rf ./students` would.

`--date GIT_DATE` checks out the repositories as of GIT\_DATE, and runs everything based on that state. Powerful, but not used much. (Theoretically, you could grade everyone's submissions as to their timeliness after the semester is over with this, but that's a bad idea.) See `man git-rev-parse` for more information on what a GIT\_DATE is.

`--workers` controls the amount of parallelization. It defaults to the number of cores in your machine. `-w1` will disable the process pool entirely, which is helpful for debugging.

## Docker Info

We have made a Docker Image for this project, which will make setting it up quite a bit easier.
To set up the project, please first make sure you have [Docker](https://www.docker.com/products/overview#/install_the_platform) installed.
Follow your particular operating system's instructions to set it up if you haven't already.

To pull the latest image of the `master` branch from Docker, (what you should probably do by default)
```console
$ docker pull stodevx/cs251-toolkit:HEAD
```

To build from source,

```console
$ # within this repository, run:
$ docker build -t <tag name>:<version> .
$ # e.g.:
$ docker build -t stodevx/cs251-toolkit:v0.0.0 .
```

Technically, you don't need to supply a version, and you can pick whatever tag name you want.  It's conventional to use `stodevx/cs251-toolkit:HEAD`, since that's what `script/run-docker` does.

To run,

```console
$ # from within the project directory---technically, you can call from any directory
$ script/run-docker <command>
$ # e.g.
$ script/run-docker cs251tk --record hw1
```

Again, tag name and version should match what you built or pulled.
If you supplied a version and you have multiple images on your system, Docker should intelligently figure out the latest version as long as you followed semantic versioning.

## Contributing
- `git clone https://github.com/StoDevX/cs251-toolkit`
- `cd cs251-toolkit`
- `python3 setup.py develop`
- go to your cs251 folder that contains the data/ and students/ folders
- run `cs251tk`, which will be the development version.


## Maintainers
There are two ways to upload a new release:

1. Automatically, through TravisCI
    - Update the version in `setup.py`
    - a) Tag a commit with that same version: `git tag v2.1.3`
    - a) Push the tag: `git push --tags`
    - b) Alternately, create a Github release with the tag name
    - Wait
    - Enjoy the new release
2. Manually, via PyPI:
    - Get a PyPI account: [pypi.org](https://pypi.org)
    - Ping @hawkrives or @rye to add you to the PyPI package
    - Run `python3 setup.py sdist upload` to generate a new release and upload it to PyPI


# Referee Documentation from CarlHacks 2017

- Make a VM (ping cluster managers)
- Install docker
- Install apache2
- Enable cgi-bin
- Add $IP (192.168.0.26)/cgi-bin/referee.sh as a PUSH webhook on a repository on Stogit
- Add the ssh key from the VM to an account on Stogit

## cron
There are somewhere around 3 crontabs.

1. (daily) Update Docker image locally on machine. Since this is a transitory process and isn’t always running, there is no downtime, per se, but requests made during a tiny interval will fail. (This is run at midnight, which is a pretty safe time.)
2. (daily) Git: Pull the toolkit. Since our scripts are run from the toolkit’s repository, we should keep this up-to-date on the server. Only the master branch is pulled.
3. (daily) Git: Pull the specs. Since the specs can change over time, we should keep them up-to-date.

The contents of these are stored in [`/script/crontab`](https://github.com/StoDevX/cs251-toolkit/blob/master/script/crontab).

# email
Referee sends email through Gmail’s smtp server, which means that we have to authenticate with gmail. Set the `CS251TK_EMAIL_USERNAME` and `CS251TK_EMAIL_PASSWORD` environment variables by way of editing the file `/home/referee/gmail_auth.sh` (which is a docker env file, not a shell script).

# env vars
- `CS251TK_EMAIL_USERNAME`: the username to authenticate to gmail with
- `CS251TK_EMAIL_PASSWORD`: the password to authenticate to gmail with

