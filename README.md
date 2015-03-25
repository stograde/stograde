# cs251-toolkit

Welcome to the CS251 toolkit, designed to help TAs and graders for St. Olaf's Software Design course.

To run:

- clone this repository
- edit the users list to be your students
- run `./update.py`

`update.py` takes several types of arguments.

```
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
```
