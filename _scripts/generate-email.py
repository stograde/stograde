#!/usr/bin/env python3

import sys
import os
import re
from add_newline_before import add_newline_before
from run_command import run

# from http://stackoverflow.com/a/16090640/2347774
def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]

def make_email(user):
	print('making email for', user)
	# Get the range of lines from '# $user' until the next line that starts with Accuracy
	# Substitute the current filename for $user (except that it just stick it in afterwards)
	# and then set it into the 'feedback' variable.
	files = [file for file in os.listdir('.') if file.startswith('hw')]
	files.sort(key=natural_sort_key)
	relevant_lines = run(['awk', '/# %s/,/^Accuracy/; sub(/%s/, FILENAME);' % (user, user)] + files, status=False)
	if not relevant_lines:
		return False

	no_user = [line for line in relevant_lines.splitlines(keepends=True) if not line.startswith('# %s' % user)]
	feedback = '\n'.join([line.replace('.mdown', '') for line in no_user])

	# our list of homeworks are the top-level headings, minus the heading octothorpe
	hws = ' '.join([line[2:] for line in feedback.splitlines(keepends=False) if line.startswith('# ')])

	email_file = '%s.eml' % (user)
	email_addr = '%s@stolaf.edu' % (user)

	plain_text_body = add_newline_before('#', feedback)
	html_body = run('pandoc -f markdown_github -t html'.split(), input=add_newline_before('#', feedback), status=False)

	email = [
		'Subject: CS251 Homework Feedback (%s)' % (hws),
		'From: Hawken Rives <rives@stolaf.edu>',
		'To: %s' % (email_addr),
		'Content-Type: multipart/mixed; boundary=0',
		'\n',
		'--0',
		'Content-Type: multipart/alternative; boundary=1',
		'\n',
		'--1',
		'Content-Type: text/plain; charset=UTF-8',
		plain_text_body,
		'--1',
		'Content-Type: text/html; charset=UTF-8',
		'\n',
		# Now we use pandoc to convert any markdown into html for the email,
		# add_newline_before is to add newlines before the hwNN headers, because awk doesn't.,
		html_body,
		'--1--',
		'--0',
		'\n',
	]

	return '\n'.join(email)


def write_email(user, email):
	with open(user + '.eml', 'w') as output:
		output.write(email)


if __name__ == '__main__':
	for user in sys.stdin:
		user = user.strip()
		email = make_email(user)
		if email:
			write_email(user, email)
