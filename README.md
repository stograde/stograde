# cs251-toolkit

Welcome to the CS251 toolkit, designed to help TAs and graders for St. Olaf's Software Design course.

Prerequisites:

- Python 3.4+
- git

To run:

- clone this repository
- put a newline-separated list of your students in `students.txt`
- run `./update.py`

The script reads from a students.txt file, by default. You can pass the `--students` argument if you only want to look at some students. It usually takes a space-separated list of students, but if given a `-`, it will also read from stdin until it hits an EOF.

The script also takes a `--record` parameter. Record does several things:

- given a folder name, it `cd`'s into that folder for each student
- it `cat`s the contents of each cpp file within the folder
- it tries to compile each `.cpp` file, and records any warnings and errors
- it runs each file, and records the output. It can also pass input to stdin during the execution
- These are controlled by the homework specs in the `specs` folder

`--record`'s logs are spit out in the `logs` folder in the current directory.

`update.py --help`:

	usage: update.py [-h] [--quiet] [--no-update] [--day DAY] [--date DATE]
	                 [--clean] [--record HW [HW ...]]
	                 [--students STUDENT [STUDENT ...]]
	                 [--sort-by {name,homework}]

	The core of the CS251 toolkit.

	optional arguments:
	  -h, --help            show this help message and exit
	  --quiet, -q           Be quieter
	  --no-update, -n       Do not update the student folders before checking.
	  --day DAY             Check out the state of the student folder as of 5pm on
	                        the last <day> (mon, wed, fri, etc).
	  --date DATE           Check out the state of the student folder as of 5pm on
	                        <date> (Y-M-D).
	  --clean               Remove student folders and re-clone them
	  --record HW [HW ...]  Record information on the student's submissions. Must
	                        be folder name to record.
	  --students STUDENT [STUDENT ...]
	                        Only iterate over these students.
	  --sort-by {name,homework}
	                        Sort by either student name or homework count.
