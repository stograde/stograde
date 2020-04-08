from bidict import bidict
import sys

from ..common import chdir, run
from ..common.run_status import RunStatus
from ..toolkit import global_vars

SPEC_URLS = bidict({
    'sd': 'https://github.com/StoDevX/cs251-specs.git',
    'hd': 'https://github.com/StoDevX/cs241-specs.git',
    'ads': 'https://github.com/StoDevX/cs253-specs.git',
    'os': 'https://github.com/StoDevX/cs273-specs.git'
})


def download_specs(course: str, basedir: str):
    course = course.split("/")[0].lower()
    try:
        url = SPEC_URLS[course]
    except KeyError:
        print("Course {} not recognized".format(course))
        sys.exit(1)
    with chdir(basedir):
        print('Downloading specs for {}'.format(course.upper()))
        status, _, _ = run(['git', 'clone', url, 'data'])
        if status is RunStatus.SUCCESS:
            print('Download complete')
        else:
            print('Download failed: {}'.format(status.name))
            sys.exit(1)


def create_data_dir(course: str, basedir: str):
    if global_vars.CI:
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
            download = input("Download specs? (y/N) ")
            if download and download.lower()[0] == "y":
                repo = input("Which class? (SD/HD/ADS/OS) ")
                if repo:
                    download_specs(repo, basedir)
                else:
                    sys.exit(1)
            else:
                print('Not downloading specs')
                sys.exit(1)


def get_supported_courses() -> str:
    course_list = [course for course in SPEC_URLS.keys()]
    courses = ''
    for course in course_list:
        courses += course + ', '
    courses = courses[:-2]
    return courses
