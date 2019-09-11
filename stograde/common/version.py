import pkg_resources  # part of setuptools

version = pkg_resources.require('stograde')[0].version
