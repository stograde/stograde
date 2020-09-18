import sys

from ..common import chdir, run
from ..common.run_status import RunStatus
from ..specs.spec_repos import get_spec_download_url, format_supported_course_list
from ..toolkit import global_vars


def download_specs(course: str, basedir: str):
    course = course.split("/")[0].upper()
    url = get_spec_download_url(course)
    with chdir(basedir):
        if not global_vars.CI:
            print('Downloading specs for {}'.format(course))
        status, result, _ = run(['git', 'clone', url, 'data'])
        if status is RunStatus.SUCCESS:
            if not global_vars.CI:
                print('Download complete')
        else:
            print('Downloading specs for {} failed: {}: {}'.format(course, status.name, result),
                  file=sys.stderr)
            sys.exit(1)


def create_data_dir(course: str, basedir: str):
    if global_vars.CI:
        if course:
            download_specs(course, basedir)
        else:
            print("data directory not found and no course specified", file=sys.stderr)
            sys.exit(1)

    else:
        print('data directory not found', file=sys.stderr)
        if course:
            download_specs(course, basedir)
        else:
            download = input("Download specs? (y/N) ")
            if download and download.lower()[0] == "y":
                repo = input("Which class? ({}) ".format(format_supported_course_list(delimiter='/')))
                if repo:
                    download_specs(repo, basedir)
                else:
                    print('Not downloading specs', file=sys.stderr)
                    sys.exit(1)
            else:
                print('Not downloading specs', file=sys.stderr)
                sys.exit(1)
