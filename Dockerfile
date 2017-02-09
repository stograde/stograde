# Use the base Python 3.6 image.  It is sufficient for accomplishing
# most of the stuff, and includes some handy build tools like gcc.
#
# NOTE This could be changed to something like `python:latest` if we
# find that there is no dependency on 3.6 itself.
FROM python:3.6

# Set the MAINTAINER flag of the docker image.
#
# NOTE Consider changing this or removing it; it is not necessary
# unless pushing to Docker Hub.
MAINTAINER Kristofer Rye <kristofer.rye@gmail.com>

# Add the entire project directory to the /cs251tk/ directory in the
# image.
ADD . /cs251tk/

# Create the SSH config directory on the root user account home directory.
RUN mkdir -p /root/.ssh/

# Build a smart SSH config (and prepare to use our id_rsa from the host)
RUN echo "Host *.stolaf.edu\n\tUserKnownHostsFile /dev/null\n\tStrictHostKeyChecking no\n\tIdentityFile /root/.ssh/id_rsa" >> /root/.ssh/config

# Lock down our SSH config
RUN chmod 600 /root/.ssh/config

# Add a marked dependency volume folder.
VOLUME /cs251tk_share/

# Change into our project directory.
WORKDIR /cs251tk

# Install the toolkit from the source directory.
RUN pip3 install .

# Update the package cache.
RUN apt-get update

# TODO Install any additional requirements.  Do we have any?
# RUN apt-get install -y cool-package

# Clean up to reduce our overall image size.
RUN apt-get clean

# Print out the versions of the installed tools.
RUN gcc --version \
    && g++ --version \
    && make --version \
    && git --version \
    && python --version

# Finally, set our default command to just "cs251tk".
CMD ["cs251tk"]
