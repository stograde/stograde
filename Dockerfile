# Use the base Python 3.6 image.  It is sufficient for accomplishing
# most of the stuff, and includes some handy build tools like gcc.
FROM python:3.6

# Set the MAINTAINER flag of the docker image.
MAINTAINER Kristofer Rye <kristofer.rye@gmail.com>

# Add the entire project directory to the /cs251tk/ directory in the
# image.
ADD . /cs251tk/

# Change into our project directory.
WORKDIR /cs251tk

# Install the toolkit from the source directory.
RUN pip3 install .

# Update the package cache.
RUN apt-get update

# RUN apt-get install -y cool-package

# Clean up to reduce our overall image size.
RUN apt-get clean

# Print out the versions of the installed tools.
RUN gcc --version \
    && g++ --version \
    && make --version \
    && python --version

# Finally, set our default command to just "cs251tk".
CMD ["cs251tk"]
