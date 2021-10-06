import sys


SPEC_REPO_NAMES = {
    'SD': 'cs251-specs',
    'HD': 'cs241-specs',
    'ADS': 'cs253-specs',
    'OS': 'cs273-specs',
    'MCA': 'cs284-specs',
}


def format_supported_course_list(delimiter: str) -> str:
    return delimiter.join(SPEC_REPO_NAMES.keys())


def github_https_clone_address(repo: str):
    return 'https://github.com/StoDevX/{}.git'.format(repo)


def github_ssh_clone_address(repo: str):
    return 'git@github.com:StoDevX/{}.git'.format(repo)


SPEC_URLS = {course: github_https_clone_address(repo) for course, repo in SPEC_REPO_NAMES.items()}


def get_spec_download_url(course: str) -> str:
    try:
        return github_https_clone_address(SPEC_REPO_NAMES[course])
    except KeyError:
        print('Invalid course: {}'.format(course), file=sys.stderr)
        sys.exit(1)


COURSE_FROM_HTTPS_URL = {github_https_clone_address(repo): course for course, repo in SPEC_REPO_NAMES.items()}
COURSE_FROM_SSH_URL = {github_ssh_clone_address(repo): course for course, repo in SPEC_REPO_NAMES.items()}
COURSE_FROM_URL = {**COURSE_FROM_HTTPS_URL, **COURSE_FROM_SSH_URL}


def get_course_from_spec_url(url: str) -> str:
    if url in COURSE_FROM_URL:
        course = COURSE_FROM_URL[url]
        print('Course {} inferred from specs'.format(course), file=sys.stderr)
        return course
    else:
        print('Could not determine course from url:', url, file=sys.stderr)
        return default_course()


def default_course() -> str:
    print('Defaulting to SD', file=sys.stderr)
    return 'SD'
