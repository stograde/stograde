# Specification (Spec) Files

A homework is defined using a specification, or spec, file.
These are located in the `data/specs` directory.

## Naming

Spec files are `.yaml` files, named after the assignment they represent.
A homework has a `hw` prefix, lab has a `lab` prefix and worksheet has a `ws` prefix.
For example, homework 1 would be specified in `hw1.yaml`, homework 15 in `hw15.yaml`, lab 5 in `lab5.yaml`, worksheet 3 in `ws3.yaml`, etc.


## Creating a Spec File

A spec file is made up of the following parts: 
- A `---`, denoting the start of the yaml file.
- An `assignment:` tag that specifies the name of the assignment (this should be the same as the filename, without the `.yaml`)
- The `compilers:` array, a list of commands that can be used to compile files (if applicable)
- The `files:` array, listing all files in the assignment, along with how to compile and test them

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

#### Compile Steps

Commands for compiling a file are specified with a `commands:` tag.
Compile steps are commonly given using the anchor-alias form.
The anchor is specified under the `compilers:` flag (see above).
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

When parsed, this becomes:

```yaml
files:
  - file: options.cpp
    commands: g++ --std=c++11 $@ -o $@.exec
```

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
- `timeout:` - Limit how long the executable can run (in seconds) before being stopped. (default: *4*)
- `truncate_contents:` - Limit how many lines of the file will be included in the log file.
- `truncate_output:` - Limit how many lines of the output will be included in the log file. (default: *10000*)
- `web:` - This file requires the SD_App React app for testing (default: *false*)

### Supporting files

Some files need extra files for compiling or testing that are the same for everyone and aren't part of the submission.
These can be added to the directory with an array under the `supporting:` tag.
A supporting file is located in `data/supporting/$ASSIGNMENT`.
Each file specified under `supporting` is copied into the directory before compiling, and removed after testing.
A different destination (such as the parent directory) can be specified with a `destination:` tag.
For example:

```yaml
supporting:
  - file: firefox.txt
  - file: react.h
    destination: ../react.h
```
