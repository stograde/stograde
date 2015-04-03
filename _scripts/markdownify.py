#!/usr/bin/env python3

import sys, os
from textwrap import indent
from .run_command import run
from .run_file import run_file

def indent4(string):
	return indent(string, '    ')

def markdownify(hw_number, username, output_type=None, to=None):
	cwd = os.getcwd()
	header = "# %s – %s" % (hw_number, username)

	files = [file for file in os.listdir('.') if file.endswith('.cpp')]
	results = []
	for file in files:
		output = []
		header = '### ' + file
		contents_header = '**contents of %s**' % (file)
		warnings_header = '**warnings about %s**' % (file)
		results_header = '**results of %s**' % (file)

		output.append(header)
		file_contents = run(['cat', file], status=False)
		output.extend([contents_header, indent4(file_contents)])

		status, compilation = run(['g++-4.8', '--std=c++11', file, '-o', '%s.exec' % (file)])
		output.extend([warnings_header, indent4(compilation)])
		if not status:
			result = run_file(hw_number, cwd + '/' + file + '.exec')
			output.extend([results_header, indent4(result)])

		results.append('\n\n'.join(output))

	[run(['rm', '-f', file + '.exec']) for file in files]

	return '# ' + hw_number + ' — ' + username + '\n' + '\n'.join(results)


if __name__ == '__main__':
	hw = sys.argv[1]
	user = sys.argv[2]
	print(markdownify(hw, user))
