from bidict import bidict
import sys

from .__main__ import CI
from ..common import chdir, run

SPEC_URLS = bidict({
    'sd': 'https://github.com/StoDevX/cs251-specs.git',
    'hd': 'https://github.com/StoDevX/cs241-specs.git',
    'ads': 'https://github.com/StoDevX/cs253-specs.git',
    'os': 'https://github.com/StoDevX/cs273-specs.git'
})


def download_specs(course: str, basedir: str) -> str:
    course = course.split("/")[0].lower()
    try:
        url = SPEC_URLS[course]
    except KeyError:
        print("Course {} not recognized".format(course))
        sys.exit(1)
    with chdir(basedir):
        print('Downloading specs for {}'.format(course.upper()))
        run(['git', 'clone', url, 'data'])
        print('Download complete')
        return course


def create_data_dir(course: str, basedir: str):
    if CI:
        if course:
            download_specs(course, basedir)
        else:
            print("data directory not found and no course specified")
            sys.exit(1)

    else:
        print('data directory not found', file=sys.stderr)
        if course:
            download_specs(course, basedir)
        else:
            download = input("Download specs? (Y/N)")
            if download and download.lower()[0] == "y":
                repo = input("Which class? (SD/HD/ADS/OS)")
                if repo:
                    download_specs(repo, basedir)
                else:
                    sys.exit(1)
            else:
                sys.exit(1)
