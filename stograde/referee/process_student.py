from stograde.student import remove
from stograde.student import clone_url
from stograde.student import checkout_ref
from stograde.student import record_student
from stograde.student import analyze_student


def process_student(*, repo, branch, assignments, folder, specs, basedir, debug=False):
    clone_url(repo, into=folder)

    try:
        # this is usually going to be a no-op (for any commits on master)
        checkout_ref(folder, ref=branch)

        recordings = record_student(folder, specs=specs, assignments=assignments, basedir=basedir, interact=False)
        analysis = analyze_student(folder, specs, check_for_branches=False)

        remove(folder)

        return analysis, recordings

    except Exception as err:
        if debug:
            raise err
        return {'username': folder, 'error': err}, []
