# Getting Started

## Installation

**Requires: Python 3.5+, git**

The toolkit *should* work on macOS, Linux and the Windows Subsystem for Linux.

The toolkit is installed using `pip`.
`pip3 install` will install something globally, but since we don't have global access on the lab machines we'll give it the `--user` flag, which installs into your home folder instead.

To install the toolkit, run `pip3 install --user stograde`.

> When you need to update the toolkit, use `pip3 install --user --no-cache --upgrade stograde`.

### PATH Note

In some cases, your path does not include the python binary directory.
Add this to your path if your command line tells you it can't find `stograde`.
This directory is located at

- `~/.local/bin` on Linux
- `~/Library/Python/3.X/bin` on maxOS, where `X` is your version (check with `python3 -V`)

Consult Google or your local unix guru for help.

## `students.txt`

The toolkit uses a file called `students.txt` to know who's repos to download.
The file is a newline-separated list of their usernames.

The students file can also include delimited sections of students using INI format, which allows the `--section section-a` arguments to work.
If no sections are provided, all students are assumed to be in the `[my]` section.

##### Basic Sample

```ini
rives
piersonv
```

##### More Involved Sample

```ini
[my]  # this is a section
rives

[section-a]  # as is this
rives
piersonv

[section-b]  # the comments aren't necessary
magnusow
```

## First Run

The toolkit expects to have a `students.txt` file and a `data` directory where it is run from.
If you don't have the `data` directory, don't worry because the toolkit will clone it for you.

Run `stograde`.
If there are multiple sections in your `students.txt`, use `stograde -a` (`-a` indicates all sections).

If you don't have a `data` directory yet, you will be asked if you want to download specs:

```
data directory not found
Download specs? (Y/N)
```

After answering with `Y`, it will then ask which class to download for:

```yaml
Which class? (SD/HD/ADS/OS)
``` 

Once you have selected a class, it will download the specs and start to clone the student repos.

When the toolkit is done cloning the repos, it will output a chart showing who has turned in at least something for each assignment.

## Common Pitfalls

### SSH Key

The terminal you are using must have the SSH key at ~/.ssh/id_rsa.pub registered with StoGit.
Otherwise you will get `[Errno 2] No such file or directory: '...'` in each line of the chart.

### Trusted Source

If this is the first time you are cloning a repo from StoGit, git/ssh will try to ask you if you want to trust the source (which kinda messes up the toolkit).
Try downloading one of your own repos separately and respond with `yes` to the prompt.
This should then register StoGit as a trusted source and it won't ask again, allowing the toolkit to work properly.
