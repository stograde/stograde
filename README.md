# cs251-toolkit

Welcome to the CS251 toolkit, designed to help TAs and graders for St. Olaf's Software Design course.

Prerequisites:

- [pandoc][pandoc]
- Python 3 (3.4+?)
- git

To run:

- clone this repository
- put a newline-separated list of your students in `students.txt`
- run `./update.py`

The script reads from a students.txt file, by default. You can pass the `--students` argument if you only want to look at some students. It usually takes a space-separated list of students, but if given a `-`, it will also read from stdin until it hits an EOF. 

The script also takes a `--record` parameter. Record does several things:

- given a folder name, it cd's into that folder for each student
- it cats out the contents of each cpp file within the folder
- it tries to compile each `.cpp` file, and records any warnings and errors
- it runs each file, and records the output. It can also pass input to stdin during the execution. 

By default, `--record` spits out markdown logs. You can use the `--output` parameter to control the output type -- it's passed straight to pandoc, so you can produce pretty much anything: PDF, latex, html, docx, odt; heck, even InDesign documents, OPML for outliners, and GROFF for man pages. See [pandoc's homepage][pandoc] for more information. 

`update.py --help`:

	~/cs251 ) ./update.py --help
	usage: update.py [-h] [--no-update] [--day DAY] [--clean]
                 [--record HW [HW ...]] [--students STUDENT [STUDENT ...]]
	
	The core of the CS251 toolkit.
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --no-update           Do not update the student folders before checking.
	  --day DAY             Check out the state of the student folder as of 5pm on
                        the last <day> (mon, wed, fri, etc).
	  --clean               Remove student folders and re-clone them
	  --record HW [HW ...]  Record information on the student's submissions. Must
                        be folder name to record.
	  --students STUDENT [STUDENT ...]
                        Only iterate over these students.

[pandoc]: http://johnmacfarlane.net/pandoc/