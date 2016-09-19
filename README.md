# cs251-toolkit

Welcome to the CS251 toolkit, designed to help TAs and graders for St. Olaf's Software Design course.

Prerequisites:

- Python 3.4+
- git

To run:

- `pip3 install --user cs251tk`
- `mkdir cs251/ && cd cs251`
- `git clone https://github.com/StoDevX/cs251-specs data`
- put a newline-separated list of your students in `students.txt`
- `cs251tk --help`

The script reads from a students.txt file, by default. You can pass the `--students` argument if you only want to look at some students (for example, `--students rives piersonv` would only work on those two students.)

The script also takes a `--record` parameter. Record does several things:

- given a folder name, it `cd`'s into that folder for each student
- it `cat`s the contents of each cpp file within the folder
- it tries to compile each `.cpp` file, and records any warnings and errors
- it runs each file, and records the output. It can also pass input to stdin during the execution
- These are controlled by the homework specs in the `specs` folder

`--record`'s logs are spit out in the `logs` folder in the current directory.

`update.py --help`:

	usage: update.py [-h] [--students USERNAME [USERNAME ...]]
	                 [--section SECTION [SECTION ...]] [--all] [--quiet]
	                 [--no-progress] [--workers N] [--sort {name,count}] [--clean]
	                 [--no-update] [--day {sun,mon,tues,wed,thurs,fri,sat}]
	                 [--date YYYY-MM-DD] [--no-check] [--record HW [HW ...]]

	The core of the CS251 toolkit

	optional arguments:
	  -h, --help            show this help message and exit

	student-selection arguments:
	  --students USERNAME [USERNAME ...]
	                        Only iterate over these students.
	  --section SECTION [SECTION ...]
	                        Only check these sections: my, all, a, b, etc
	  --all                 Shorthand for '--section all'

	optional arguments:
	  --quiet, -q           Don't show the table
	  --no-progress         Hide the progress bar
	  --workers N, -w N     The number of operations to perform in parallel
	  --sort {name,count}   Sort the students table

	student-folder arguments:
	  --clean               Remove student folders and re-clone them
	  --no-update, -n       Do not update the student folders when checking

	time-based arguments:
	  --day {sun,mon,tues,wed,thurs,fri,sat}
	                        Check out submissions as of 5pm on WEEKDAY
	  --date YYYY-MM-DD     Check out submissions as of 5pm on DATE

	grading arguments:
	  --no-check, -c        Do not check for unmerged branches
	  --record HW [HW ...]  Record information on student submissions. Requires a
	                        spec file


## Contributing
- `git clone <this_repo>`
- `cd cs251-toolkit`
- `pyvenv ./venv`
- `source ./venv/bin/activate`
- `python3 setup.py develop`
- go to your cs251 folder that contains the data/ and students/ folders
- run `cs251tk`; it'll be the development version.
- run `deactivate` to leave the venv.


## Maintainers
- You need a PyPI account: [pypi.org](https://pypi.org)
- `python3 setup.py sdist upload` shoudl generate a new release and upload it to PyPI
