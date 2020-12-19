# Contributing to `stograde`

## Creating a New Release

The release process for StoGrade is quite simple, yet does have a few steps:

- Create a new branch with the version name, e.g. `git checkout -b v2.1.3`
- Update the version in `setup.py` (Make sure you understand [semantic versioning](https://packaging.python.org/guides/distributing-packages-using-setuptools/#semantic-versioning-preferred) first!)
- Commit the modification to `setup.py`
  - Don't include anything else in this branch, just the version change
- Tag the commit with that same version, e.g. `git tag v2.1.3`
- Push the commit and tag: `git push --tags`
- Quickly go to GitHub and create a new release (you need to do it before the CI/CD process gets to deployment to PyPI, where it compares the tag to the latest release)
- Wait
- Enjoy the new release


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

`stograde` uses [Travis CI](https://travis-ci.com) for its CI/CD (Continuous Integration/Continuous Deployment) pipelines.
The pipelines are configured in the [.travis.yml](.travis.yml) file.

- Stages labeled `test` are used to test `stograde` to make sure it is working as we expect.
It tests against python versions 3.6-3.8 (as of v4.2.1).
- Stages labeled `deploy docker` handle building and pushing docker images to [dockerhub](https://hub.docker.com/r/stodevx/stograde).
The actual docker build is done by the [docker-deploy](script/docker-deploy) script.
- The stage labeled `deploy pypi` handles pushing a new version of `stograde` to [PyPI](https://pypi.org/project/stograde/).
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

*Note that, for whatever reason, the combination of the `gcc:latest` image plus the ARM build leads to a docker build that takes about 20 minutes. It seems like the python regex library may be partially to blame as it takes about 13 minutes to build.*

The docker builds happen as part of the CI/CD process.

