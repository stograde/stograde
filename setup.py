from setuptools import setup, find_packages

setup(
    name='cs251tk',
    version='2.0.3',
    description='The CS251 (Software Design) Toolkit',
    author='Hawken Rives',
    author_email='hawkrives@gmail.com',
    url='https://github.com/stodevx/cs251-toolkit',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

    ],
    keywords='stolaf course-tooling',
    install_requires=[
        'PyYAML == 3.*',
        'requests == 2.*',
        'termcolor == 1.*',
        'update_checker == 0.12',
    ],
    tests_require=['tox'],
    packages=find_packages(exclude=['tests', 'docs']),
    # see http://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    entry_points={
        'console_scripts': [
            'cs251tk=cs251tk.cs251tk:main',
        ],
    },
)
