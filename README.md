# stograde
[![PyPI](https://img.shields.io/pypi/v/stograde.svg)](https://pypi.python.org/pypi/stograde)
[![TraviCI](https://travis-ci.org/StoDevX/stograde.svg?branch=master)](https://travis-ci.org/StoDevX/stograde)
[![Coverage Status](https://coveralls.io/repos/github/StoDevX/stograde/badge.svg?branch=master)](https://coveralls.io/github/StoDevX/stograde?branch=master)

Welcome to the StoGrade toolkit, designed to help TAs and graders for St. Olaf's Computer Science courses.

## Usage

This toolkit gives you the power to do a bunch of things, including

- simply manage a set of student repositories (`stograde repo ...`)
- check which assignments the students have turned in (`stograde table`)
- run tests against those assignments and produce a log file for grading (`stograde record`)
- view programs one at a time in the SD_app React app (`stograde web`)
- check a student's submissions as part of an automatic GitLab CI job (`stograde ci`)

**To get started, take a look at the [Getting Started](docs/GETTING_STARTED.md) guide.**

For more details, take a look at the documentation pages for:
- [Recording Assignments with `stograde record`](docs/RECORD.md)
- [Getting an Overview of Submissions with `stograde table`](docs/TABLE.md)
- [Grading React App Files with `stograde web`](docs/WEB.md)
- [Managing Student Repositories with `stograde repo`](docs/REPO.md)
- [Using StoGrade in a GitLab CI Job with `stograde ci`](docs/CI.md)
- [Creating and Understanding Spec Files](docs/SPECS.md)

## Docker Info

We have made a Docker Image for this project, which will make setting it up quite a bit easier.
To set up the project, please first make sure you have [Docker](https://www.docker.com/products/overview#/install_the_platform) installed.
Follow your particular operating system's instructions to set it up if you haven't already.

To pull the latest image of the `master` branch from Docker, (what you should probably do by default)
```console
$ docker pull stodevx/stograde:HEAD
```

To build from source,

```console
$ # within this repository, run:
$ docker build -t <tag name>:<version> .
$ # e.g.:
$ docker build -t stodevx/stograde:v0.0.0 .
```

Technically, you don't need to supply a version, and you can pick whatever tag name you want.  It's conventional to use
`stodevx/stograde:HEAD`, since that's what `script/run-docker` does.

To run,

```console
$ # from within the project directory---technically, you can call from any directory
$ script/run-docker <command>
$ # e.g.
$ script/run-docker stograde --record hw1
```

Again, tag name and version should match what you built or pulled.
If you supplied a version and you have multiple images on your system, Docker should intelligently figure out the latest
version as long as you followed semantic versioning.

## Contributing
- `git clone https://github.com/StoDevX/stograde`
- `cd stograde`
- `python3 setup.py develop`
- go to your grading folder that contains the data/ and students/ folders
- run `stograde`, which will be the development version.


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

1. (daily) Update Docker image locally on machine. Since this is a transitory process and isn’t always running, there is
no downtime, per se, but requests made during a tiny interval will fail. (This is run at midnight, which is a pretty safe
time.)
2. (daily) Git: Pull the toolkit. Since our scripts are run from the toolkit’s repository, we should keep this up-to-date
on the server. Only the master branch is pulled.
3. (daily) Git: Pull the specs. Since the specs can change over time, we should keep them up-to-date.

The contents of these are stored in [`/script/crontab`](https://github.com/StoDevX/stograde/blob/master/script/crontab).

# email
Referee sends email through Gmail’s smtp server, which means that we have to authenticate with gmail. Set the
`STOGRADE_EMAIL_USERNAME` and `STOGRADE_EMAIL_PASSWORD` environment variables by way of editing the file
`/home/referee/gmail_auth.sh` (which is a docker env file, not a shell script).

# env vars
- `STOGRADE_EMAIL_USERNAME`: the username to authenticate to gmail with
- `STOGRADE_EMAIL_PASSWORD`: the password to authenticate to gmail with

