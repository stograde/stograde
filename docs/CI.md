# Using StoGrade in a GitLab CI Job with `stograde ci`

The toolkit has built-in support for automated testing of a student's code with GitLab CI.
A `.gitlab-ci.yml` file has to be added to the root of their repository ([examples below](#gitlab-ciyml)).
If an assignment needs to be excluded from testing, its name can be added to a [`.stogradeignore` file](#stogradeignore).

## Functionality

When running a CI job:
- The toolkit will first determine the student and course based on GitLab environment variables.
- It will then determine which assignments to check based on the directories in the student's repository.
- The toolkit will then check that all the files are present as well as try compiling them.
*It will not run any tests on them, only attempt to compile them.*
- If anything is amiss, it will print out warnings letting the student know what's wrong with their assignment, then fail the job, and thus the whole pipeline.
  - This will prompt GitLab to send an email to the student who started the pipeline with their `git push` telling them that their pipeline failed.

If a file is not required, the `optional: true` option can be added to the file in the spec.
Thus if it is missing, the build will not fail.
If the file doesn't have to compile successfully for it to pass, then `optional_compile: true` option can be added.

## Configuration

### `.stogradeignore`

If a student is having their pipeline fail due to an old assignment that they aren't going to go back and fix, that assignment can be ignored.
Simply add the assignment id to a new line in a `.stogradeignore` file.

For example, to ignore homework 8, lab 2 and worksheet 4, the `.stogradeignore` would look like this:

```
hw8
lab2
ws4
```

### `.gitlab-ci.yml`

The `.gitlab-ci.yml` file is what tells GitLab how to run its pipelines for the repository.
We configure it to download a Docker image with StoGrade installed and run `stograde ci`.
(See the [GitLab documentation](https://docs.gitlab.com/ee/ci/yaml/) for more information about how the `.gitlab-ci.yml` file works.)

#### Software Design

Because Software Design uses the React App, it needs a few extra libraries to be included.
Thus it uses the `-gcc` version of the docker images, which are based off of the `gcc:latest` docker image (instead of the `python:3-slim` image).

```yaml
image: stodevx/stograde:latest-gcc
stograde:
    stage: stograde
    script:
        - stograde ci
```

##### Software Design with GCloud

The Software Design students add a Google Cloud integration into their repositories partway through the semester.
They do this by changing the `.gitlab-ci.yml` file.
This configuration will first run the stograde checks on their homework, and then if that passes will run the deployment to Google Cloud.
Note that the `allow_failure: true` line under `gcloud` allows the `gcloud` section of the pipeline to fail without failing the whole pipeline.
When the whole pipeline fails is when the student gets an email.

```yaml
stages:
  - stograde
  - gcloud

stograde:
    stage: stograde
    image: stodevx/stograde:latest-gcc
    script:
        - stograde ci
        
gcloud:
    stage: gcloud
    allow_failure: true
    image: docker.cs.stolaf.edu:443/sd_managers/sd-backend:latest
    script: "source /SD-backend/deploy.sh $PROJECT_ID"
```

#### Hardware Design

Because Hardware Design uses ARM assembly, the default runner on thing3 is unable to test their assembly code from late in the semester.
Thus, we add the `rasperrypi` label which tells it to use a runner with the `raspberrypi` label if possible.

```yaml
image: stodevx/stograde:latest
stograde:
    stage: stograde
    labels:
        - raspberrypi 
    script:
        - stograde ci
``` 

#### Other Courses

Any other course that doesn't require special accommodations can use this config:

```yaml
image: stodevx/stograde:latest
stograde:
    stage: stograde
    script:
        - stograde ci
```
