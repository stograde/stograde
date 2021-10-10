# Use the base Python slim image.  It is sufficient for accomplishing
# most of the stuff, and includes some handy build tools like gcc.
FROM python:3-slim

# Set the MAINTAINER flag of the docker image.
#
# NOTE Consider changing this or removing it; it is not necessary
# unless pushing to Docker Hub.
MAINTAINER Kristofer Rye <kristofer.rye@gmail.com>

# Update the package cache.
RUN apt-get update

# Install any additional requirements.
RUN apt-get install -y gcc git g++ make

# Add the entire project directory to the /stograde/ directory in the
# image.
ADD . /stograde/

## Create the SSH config directory on the root user account home directory.
#RUN mkdir -p /root/.ssh/
#
## Build a smart SSH config (and prepare to use our id_rsa from the host)
#RUN echo "Host *.stolaf.edu\n\tUserKnownHostsFile /dev/null\n\tStrictHostKeyChecking no\n\tIdentityFile /root/.ssh/id_rsa" >> /root/.ssh/config
#
## Lock down our SSH config
#RUN chmod 600 /root/.ssh/config
#
## Add a marked dependency volume folder.
#VOLUME /stograde_share/
#
## Change into our project directory.
#WORKDIR /stograde
#
## Make a symlink between /stograde_share/blah and /stograde/blah
#RUN ln -sv /stograde_share/data /stograde/data
#RUN ln -sv /stograde_share/students /stograde/students
#RUN ln -sv /stograde_share/logs /stograde/logs
#RUN ln -sv /stograde_share/students.txt /stograde/students.txt
#
## Make symlinks for our SSH keys.
#RUN ln -sv /stograde_share/.ssh/id_rsa /root/.ssh/id_rsa
#RUN ln -sv /stograde_share/.ssh/id_rsa.pub /root/.ssh/id_rsa.pub

# Install the toolkit from the source directory.
RUN --mount=type=cache,target=/tmp/.pip-cache pip3 install .

# Print out the versions of the installed tools.
RUN gcc --version \
    && g++ --version \
    && make --version \
    && git --version \
    && python3 --version

# Finally, set our default command to just "stograde".
CMD ["stograde"]
