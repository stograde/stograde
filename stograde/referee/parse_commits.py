from cs251tk.common import parse_commit_msg_for_assignments
from cs251tk.common import flatten
from natsort import natsorted


def parse_commits_for_assignments(commits):
    """Takes a list of commits and returns the affected assignments

    Input is a commit message; it returns a list of (hw|lab, ##) tuples.

    A commit looks like the following:

    {
      "id": "b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
      "message": "Update Catalan translation to e38cb41.",
      "timestamp": "2011-12-12T14:27:31+02:00",
      "url": "http://example.com/mike/diaspora/commit/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
      "author": {
        "name": "Jordi Mallach",
        "email": "jordi@softcatala.org"
      },
      "added": ["CHANGELOG"],
      "modified": ["app/controller/application.rb"],
      "removed": []
    }

    Tested on these commit messages:
        - 'hw13 complete; part of hw14'
        - [more messages in test/assignment_parsing_test]
    """
    assignments = [parse_commit_msg_for_assignments(c['message']) for c in commits]
    return natsorted(set(flatten(assignments)))
