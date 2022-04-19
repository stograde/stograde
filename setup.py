import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    sys.exit("The toolkit requires Python 3.6 or greater.\nYou have {}".format(sys.version_info))

install_requires = [
    'PyYAML >= 5,< 7',
    'requests >= 2.20.*',
    'termcolor == 1.*',
    'natsort>=7.1,<8.2',
    'appdirs == 1.4.*',
    'python-dateutil >= 2.7,< 2.9',
    'PyInquirer == 1.0.*',  # required by stograde web
    'google-api-python-client>=2.24,<2.46',  # required by stograde drive
    'google-auth-oauthlib == 0.4.*',  # required by stograde drive
    'six >= 1.13.0',  # required by google-api-core
    'setuptools >= 40.3.0',  # required by google-auth
]

# This allows us to use dataclasses in python 3.6
if sys.version_info < (3, 7):
    install_requires.append('dataclasses >= 0.6')

setup(
    name='stograde',
    version='4.4.0',
    description='The StoGrade Toolkit',
    author='Hawken Rives',
    author_email='hawkrives@gmail.com',
    url='https://github.com/stograde/stograde',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='stolaf course-tooling',
    install_requires=install_requires,
    tests_require=['tox', 'pytest'],
    packages=find_packages(exclude=['tests', 'docs']),
    # see http://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    entry_points={
        'console_scripts': [
            'stograde=stograde.toolkit.__main__:main',
            'referee=stograde.referee.__main__:main',
        ],
    },
)
