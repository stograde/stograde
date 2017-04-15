from cs251tk.student import remove
from cs251tk.student import clone_url
from cs251tk.student import checkout_ref
from cs251tk.student import record
from cs251tk.student import analyze


def process_student(*, repo, branch, assignments, folder, specs, basedir, debug=False):
    clone_url(repo, into=folder)

    try:
        # this is usually going to be a no-op (for any commits on master)
        checkout_ref(folder, ref=branch)

        recordings = record(folder, specs=specs, to_record=assignments, basedir=basedir, debug=debug, interact=False)
        analysis = analyze(folder, specs, check_for_branches=False)

        remove(folder)

        return analysis, recordings

    except Exception as err:
        if debug:
            raise err
        return {'username': folder, 'error': err}, []
