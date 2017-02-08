FROM python:3.6

MAINTAINER Kristofer Rye <kristofer.rye@gmail.com>

ADD . /cs251tk/

WORKDIR /cs251tk

RUN pip3 install .

RUN apt-get update

# RUN apt-get install -y cool-package

RUN apt-get clean

RUN gcc --version \
    && g++ --version \
    && make --version \
    && python --version

CMD ["cs251tk"]
