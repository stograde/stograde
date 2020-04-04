# CI

The toolkit has built-in support for automated testing of a student's code with GitLab CI.
A `.gitlab-ci.yml` file has to be added to the root of their repository.

## Configuration

### Software Design

Because Software Design uses the React App, it needs a few extra libraries to be included.
Thus it uses the `-gcc` version of the docker images, which are based off of the `gcc:latest` docker image (instead of the `python:3-slim` image).

```yaml
image: stodevx/stograde:latest-gcc
build:
    stage: build
    script:
        - stograde --ci
```

### Software Design with GCloud

The Software Design students add a Google Cloud integration into their repositories partway through the semester.
They do this by changing the `.gitlab-ci.yml` file.
This configuration will first run the stograde checks on their homework, and then if that passes will run the deployment to Google Cloud.

```yaml
stages:
  - stograde
  - gcloud

stograde:
    stage: stograde
    image: stodevx/stograde:latest-gcc
    script:
        - stograde --ci
        
gcloud:
    stage: gcloud
    image: docker.cs.stolaf.edu:443/sd_managers/sd-backend:latest
    script: "source /SD-backend/deploy.sh $PROJECT_ID"
```

### Hardware Design

Because Hardware Design uses ARM assembly, the default runner on thing3 is unable to test their assembly code from late in the semester.
Thus, we add the `rasperrypi` label which tells it to use a runner with the `raspberrypi` label if possible.

```yaml
image: stodevx/stograde:latest
build:
    stage: build
    labels:
        - raspberrypi 
    script:
        - stograde --ci
``` 

### Other Courses

Any other course that doesn't require special accommodations can use this config:

```yaml
image: stodevx/stograde:latest
build:
    stage: build
    script:
        - stograde --ci
```
