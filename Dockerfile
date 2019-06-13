# Use the base Python 3.6 image.  It is sufficient for accomplishing
# most of the stuff, and includes some handy build tools like gcc.
#
# NOTE This could be changed to something like `python:latest` if we
# find that there is no dependency on 3.6 itself.
FROM python:3-slim

# Set the MAINTAINER flag of the docker image.
#
# NOTE Consider changing this or removing it; it is not necessary
# unless pushing to Docker Hub.
MAINTAINER Kristofer Rye <kristofer.rye@gmail.com>

# Add the entire project directory to the /stograde/ directory in the
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

# Make a symlink between /cs251tk_share/blah and /stograde/blah
RUN ln -sv /cs251tk_share/data /cs251tk/data
RUN ln -sv /cs251tk_share/students /cs251tk/students
RUN ln -sv /cs251tk_share/logs /cs251tk/logs
RUN ln -sv /cs251tk_share/students.txt /cs251tk/students.txt

# Make symlinks for our SSH keys.
RUN ln -sv /cs251tk_share/.ssh/id_rsa /root/.ssh/id_rsa
RUN ln -sv /cs251tk_share/.ssh/id_rsa.pub /root/.ssh/id_rsa.pub

# Update the package cache.
RUN apt-get update

# TODO Install any additional requirements.  Do we have any?
RUN apt-get install -y gcc git g++ make

# Install the toolkit from the source directory.
RUN pip3 install .

# Print out the versions of the installed tools.
RUN gcc --version \
    && g++ --version \
    && make --version \
    && git --version \
    && python --version

# Finally, set our default command to just "stograde".
CMD ["cs251tk"]
