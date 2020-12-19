# stograde
[![PyPI](https://img.shields.io/pypi/v/stograde.svg)](https://pypi.python.org/pypi/stograde)
[![TraviCI](https://travis-ci.org/StoDevX/stograde.svg?branch=master)](https://travis-ci.org/StoDevX/stograde)
[![Coverage Status](https://coveralls.io/repos/github/StoDevX/stograde/badge.svg?branch=master)](https://coveralls.io/github/StoDevX/stograde?branch=master)

Welcome to the StoGrade toolkit, designed to help TAs and graders for St. Olaf's Computer Science courses.

## Usage

This toolkit gives you the power to do a bunch of things, including

- simply manage a set of student repositories (`stograde repo ...`)
- check which assignments the students have turned in (`stograde table`)
- get a list of URLs for assignments submitted via Google Drive (`stograde drive`)
- run tests against those assignments and produce a log file for grading (`stograde record`)
- view programs one at a time in the SD_app React app (`stograde web`)
- check a student's submissions as part of an automatic GitLab CI job (`stograde ci`)

**To get started, take a look at the [Getting Started](docs/GETTING_STARTED.md) guide.**

For more details, take a look at the documentation pages for:
- [Recording Assignments with `stograde record`](docs/RECORD.md)
- [Checking Google Drive Submissions with `stograde drive`](docs/DRIVE.md)
- [Getting an Overview of Submissions with `stograde table`](docs/TABLE.md)
- [Grading React App Files with `stograde web`](docs/WEB.md)
- [Managing Student Repositories with `stograde repo`](docs/REPO.md)
- [Using StoGrade in a GitLab CI Job with `stograde ci`](docs/CI.md)
- [Creating and Understanding Spec Files](docs/SPECS.md)


## Contributing

View the [contribution documentation](CONTRIBUTING.md).
