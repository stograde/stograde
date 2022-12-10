# Contributing to `stograde`

## Starting to Develop for StoGrade

- `git clone https://github.com/stograde/stograde`
- `cd stograde`
- `python3 setup.py develop`
- go to your grading folder that contains the data/ and students/ folders
- run `stograde`, which will be the development version.


## Creating a New Release

The release process for StoGrade is quite simple, yet does have a few steps:

- Create a new branch with the version name, e.g. `git checkout -b v2.1.3`
    - The name of the new branch should begin with a 'v' e.g 'v4.4.0' 
- Update the version in `setup.py` (Make sure you understand [semantic versioning](https://packaging.python.org/guides/distributing-packages-using-setuptools/#semantic-versioning-preferred) first!)
- Commit the modification to `setup.py`
    - Don't include anything else in this branch, just the version change
- Push the commit
- Create a new release based on the branch
  - **Enter the version name for the tag**
  - **Enter the version name for the target branch**
- Wait for GitHub Actions release to complete
- Merge branch into `main`
- Enjoy the new release


## Testing

StoGrade uses pytest and tox for testing.
To run tests, run the command `tox` from the root directory of the project.

To skip integration tests (those located in `test/integration_tests`) which take a while to run, add the `SKIP_E2E` environment variable to your command like this: `SKIP_E2E="yes" tox`.

Tests is an important part of any codebase, and StoGrade is no different.
StoGrade comes with hundreds of tests that test every aspect of the codebase.

[![Coverage Status](https://coveralls.io/repos/github/stograde/stograde/badge.svg?branch=main)](https://coveralls.io/github/stograde/stograde?branch=main)

The 100% test coverage badge in the README (and above) indicates that every line of code in StoGrade is run at least once during testing, or is ignored from coverage.
As new code is added to StoGrade, tests should be written to test it and verify that it works, keeping that coverage at 100%.
Here is a [good article](https://www.dein.fr/2019-09-06-test-coverage-only-matters-if-at-100-percent.html) about why to do this.

The `referee` module is ignored because that codebase is not actively maintained and the `webapp/server.py` file is ignored because it is a copy-paste of the file used by students in Software Design.
We also ignore any blocks of code within a `if TYPE_CHECKING:` guard because lines within those blocks are only run when the code is being edited and never when the code is being run.


## Tips for Understanding the Codebase

`stograde` is a large program, split into multiple modules, that can be difficult to understand at times.

### Modules

`stograde` (as of version `4.2.1`) has 10 separate modules:

- `common` - methods used throughout the program, such as `run`, `chdir`, etc.
- `drive` - functionality associated with `stograde drive`
- `formatters` - formatting, such as creating the markdown or html output, creating the table, etc.
- `process_assignment` - processing the assignment and all classes associated with that process
- `process_file` - processing a single file in a student's submission
- `referee` - contains the codebase used with the old referee program (not actively maintained because of the introduction of `stograde ci`)
- `specs` - everything that you need for processing spec files
- `student` - handles processing, recording and analyzing a single student's submission, as well as managing our copy of their git repo
- `toolkit` - the entry point into the program and other miscellaneous functionality
- `webapp` - functionality associated with `stograde web`

### CI/CD

`stograde` uses [GitHub Actions](https://github.com/features/actions) for its CI/CD (Continuous Integration/Continuous Deployment) workflows.
The pipelines are configured in [pull_request.yml](.github/workflows/pull_request.yml) and [push.yml](.github/workflows/push.yml).

- The `test` job is used to test `stograde` to make sure it is working as we expect.
It uses a matrix to test against python versions 3.6-3.9 (as of v4.4.3).
- The `docker` job handles building and pushing docker images to the [GitHub container registry](https://github.com/stograde/stograde/pkgs/container/stograde)
- The `pypi` job handles pushing a new version of `stograde` to [PyPI](https://pypi.org/project/stograde/).
This only happens for tagged commits that are tagged with the tag associated with the most recent release.

### Dockerfiles

`stograde` has two Dockerfiles.
This is because of the requirements of the Software Design course's SD_app.

- The main [Dockerfile](Dockerfile) is based on the `python:3-slim` image and is sufficient for almost all uses.
- The second [Dockerfile.gcc](Dockerfile.gcc) is based on the `gcc:latest` image and is used for any Software Design GitLab runners.

The only differences are the base image and what is installed by `apt-get`.
The `python:3-slim` image doesn't include `gcc`, `g++`, `git` or `make`, so we install those.
The `gcc:latest` image doesn't include python development packages, so we install those.

The reason for the distinction is because compiling programs for the Software Design app would throw errors with the normal image, and the workaround was to make two docker images available.
The image based on the `gcc:latest` image always has the suffix `-gcc`.

The docker build process for `stograde` uses the `docker buildx` multiplatform functionality.
This is because the Hardware Design course uses ARM-based GitLab runners, which the default AMD-based image would not work with.
So we create two versions of each image (though they are called the same thing), one for AMD and one for ARM.
Docker is smart enough to pick the correct one for the architecture it is running on.

Docker layer caching is set up to decrease the build time from ~8 minutes to ~2 minutes when the cache is present.
The long part of the build process is installing the python dependencies on ARM, therefore the installation of `apt` and `pip` packages happens first in the dockerfiles to allow those steps to be cached
If `setup.py` changes, the pip installation layer in the cache is invalidated, and the step is performed again.

The docker builds happen as part of the CI/CD process.
The final container images are added to the [stograde package](https://github.com/stograde/stograde/pkgs/container/stograde).

