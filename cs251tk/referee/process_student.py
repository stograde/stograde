from cs251tk.student import remove
from cs251tk.student import clone_url
from cs251tk.student import checkout_ref
from cs251tk.student import record
from cs251tk.student import analyze


def process_student(repo, branch, assignments, folder, specs, basedir):
    clone_url(repo)

    try:
        # this is usually going to be a no-op (for any commits on master)
        checkout_ref(folder, ref=branch)

        recordings = record(folder, specs, record=assignments, basedir=basedir)
        analysis = analyze(folder, specs, check_for_branches=False)

        remove(folder)

        return analysis, recordings

    except Exception as err:
        return {'username': folder, 'error': err}, []
