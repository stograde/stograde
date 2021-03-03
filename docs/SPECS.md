# Specification (Spec) Files

How each homework gets checked is defined using a specification (or spec) file.
These are located in the `data/specs` directory.

To jump to the explanation of a specific tag, follow the following links:
- [`assignment:`](#Creating-a-Spec-File)
- [`folder:`](#Testing-a-Different-Directory)
- [`architecture:`]()
- [`compilers:`](#Compilers)
- [`files:`](#Files)
  - [`file:`](#Files)
  - [`alternates:`](#Alternate-Names)
  - [`commands:`](#Compile-Steps)
  - [`tests:`](#Test-Steps)
  - [`options:` (and its child tags)](#Options)
- [`supporting:`](#Supporting-Files)
- [`inputs:`](#Input-Files)


## Naming

Spec files are `.yaml` files, named after the assignment they represent.
A homework has a `hw` prefix, lab has a `lab` prefix and worksheet has a `ws` prefix.
For example, homework 1 would be specified in `hw1.yaml`, homework 15 in `hw15.yaml`, lab 5 in `lab5.yaml`, worksheet 3 in `ws3.yaml`, etc.

## Creating a Spec File

A spec file is made up of the following parts: 
- A `---`, denoting the start of the yaml file.
- An `assignment:` tag that specifies the name of the assignment (this should be the same as the filename, without the `.yaml`)
- Any extra properties about the assignment, such as `folder:` or `architecture:`
- The `compilers:` array, a list of commands that can be used to compile files (if applicable)
- The `files:` array, listing all files in the assignment, along with how to compile and test them

#### Testing a Different Directory

If you want to test a directory other than the one that would be used by default (named after the assignment), you can add a `folder:` tag.
The value will be used in place of the assignment's name when `cd`ing into the student's directory.
For example, a `folder: images` line in homework 15 will have the toolkit `cd` into `images` instead of `hw15` when checking a student's assignment.

#### Testing on a Specific Architecture

When you are compiling assembly code, you can't compile it just anywhere - it has to be compatible with your system's architecture.
To prevent extraneous warnings and errors caused by compiling on the wrong architecture, spec files support an `architecture:` tag.
The architecture is checked using `uname -m` and the result is compared to the value of `architecture:`.
If `architecture:` is not present, then it is assumed that the code is not dependent on a specific architecture.
The main use of this is in Hardware Design when students start writing ARM assembly.
The HD specs that contain assembly add `architecture: armv7l` (note the `v7l` at the end) to specify that the ARM architecture is required.

When the architecture is incompatible:
- if the toolkit is running as part of a CI job, it will print a notice that it is skipping the assignment because of `wrong architecture`
- otherwise it will print a warning that the assignment requires the specific architecture and will tell you what architecture you have 

### Compilers

Commands used to compile files can be specified using anchor-alias form.
The anchors are listed in an array under `compilers:`.
An anchor is identified with `&name '...'`.
This copies the anchor into the place where the alias is located.

#### Variables in Commands

The target of the command can be inserted into the command with `$@`.
Whenever a `$@` is encountered, the `$@` is replaced with the filename.
For example, if the command is `cat $@` and the filename is `test.txt`, the command will become `cat test.txt`.

#### Common Compilers

- C++ file: `gcc --std=c++11 $@ -o $@.exec`
- React App file: `gcc --std=c++11 $@ react.o -lcurl`

### Files

Files are listed in an array under a `files:` tag.
Each filename is specified with `file: name`.
For example:

```yaml
files:
  - file: hw1.txt
  - file: Dog.cpp
  - file: Dog.h
  - file: tryDog.cpp
```

#### Alternate Names

If a student turns in a file but it is not named properly, it will not be detected by StoGrade.
If there is a file that multiple students have or may misname, this can be accommodated for in the spec file.
Using the `alternates:` tag, one or more alternate names for the file can be given.
For example:

```yaml
files:
  - file: Dog.cpp
    alternates: dog.cpp
  - file: Dog.h
    alternates:
      - dog.h
      - cat.h
```

If alternate names are given and more than one name has a matching file, then a warning will be printed in the recording alerting the grader that the file the student intended to turn in may not be the one shown in the recording.


#### Compile Steps

Commands for compiling a file are specified with a `commands:` tag.
Compile steps are commonly given using the anchor-alias form.
The anchor is specified under the `compilers:` tag (see above).
The alias for the anchor is `*name`.
This copies the anchor into the place where the alias is located.
For example:

```yaml
compilers:
  - &cpp 'g++ --std=c++11 $@ -o $@.exec

files:
  - file: options.cpp
    commands: *cpp
```

When the yaml is parsed, this becomes:

```yaml
files:
  - file: options.cpp
    commands: g++ --std=c++11 $@ -o $@.exec
```

When the compile command is parsed before being run, it becomes `gcc --std=c++11 options.cpp -o options.cpp.exec`
(explained above under [Variables in Commands](#Variables-in-Commands)).

#### Test Steps

Test commands are specified just like compile commands but with a `tests:` tag.
Continuing the example from above:

```yaml
compilers:
  - &cpp 'g++ --std=c++11 $@ -o $@.exec

files:
  - file: options.cpp
    commands: *cpp
    tests: $@.exec
```

#### Options

- `hide_contents:` - Don't include the contents of the file in the log output. (default: *false*)
- `optional:` - The file isn't required for the assignment to be complete.
If missing, the file will have  (**optional submission**) in the log file and will not fail any CI jobs. (default: *false*)
- `optional_compile:` - The file doesn't have to compile for the CI job to pass. (default: *false*)
- `timeout:` - Limit how long the executable can run (in seconds) before being stopped. (default: *4.0*)
- `truncate_contents:` - Limit how many lines of the file will be included in the log file. (default: *10000*)
- `truncate_output:` - Limit how many lines of the output will be included in the log file. (default: *10000*)
- `web:` - This file requires the Software Design React app for testing (default: *false*)

Continuing the example from above:

```yaml
compilers:
  - &cpp 'g++ --std=c++11 $@ -o $@.exec

files:
  - file: options.cpp
    commands: *cpp
    tests: $@.exec
    options:
      web: true
      optional: true
```

### Supporting Files

Some files need extra files for compiling or testing that are the same for everyone and aren't part of the submission.
These can be added to the directory with an array under the `supporting:` tag.
A supporting file is located in `data/supporting/$ASSIGNMENT`.
Each file specified under `supporting` is copied into the directory before compiling, and removed after testing.
A different destination (such as the parent directory) can be specified with a `destination:` tag.
For example:

```yaml
supporting:
  - file: react.o
  - file: react.h
    destination: ../react.h
```

### Input Files

Some files are used as input while testing an executable.
These can be added to the directory with an array under the `inputs:` tag.
An input file is located in `data/supporting/$ASSIGNMENT`.
Each file specified under `inputs` is copied into the directory before compiling, and removed after testing.
A different destination (such as the parent directory) can be specified with a `destination:` tag.
For example:

```yaml
inputs:
  - file: in.txt
```

#### Supporting vs Input Files

You may notice that the descriptions for `supporting` and `inputs` are very similar.
This is because the `inputs:` tag has the exact same functionality as the `supporting:` tag, so they technically can be used interchangeably.
The distinction is mainly for clarity about what the file is being used for, as well as backward compatibility with old specs.
(i.e. header files like `react.h` would be listed under `supporting` while input files like `in.txt` would be listed under `inputs`.)
