# Use the base Python slim image
FROM python:3-slim

# Update the package cache
RUN apt-get update

# Install any additional requirements
RUN apt-get install -y gcc git g++ make

# Create a working directory
WORKDIR /stograde

# Copy setup.py into directory
ADD ./setup.py /stograde/setup.py

# Create a requires.txt file from setup.py
RUN python3 setup.py egg_info

# Use requires.txt to install dependencies
# This allows everything up to this point to be cached if
#  setup.py doesn't change
RUN pip install -r stograde.egg-info/requires.txt

# Add the entire project directory to the /stograde/ directory
ADD . /stograde/

# Install the toolkit from the source directory
RUN pip3 install .

# Print out the versions of the installed tools
RUN gcc --version \
    && g++ --version \
    && make --version \
    && git --version \
    && python3 --version

# Finally, set our default command to just "stograde"
CMD ["stograde"]
