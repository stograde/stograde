#!/usr/bin/env python3

import sys, os
from .flatten import flatten
from textwrap import indent
from .run_command import run
from .run_file import run_file

def indent4(string):
	return indent(string, '    ')

def markdownify(hw_number, username, spec, output_type=None, to=None):
	cwd = os.getcwd()
	results = []

	for input, contents in spec.get('inputs', {}).items():
		with open(cwd + '/' + input, 'w') as outfile:
			outfile.write(contents)

	for file in spec['files']:
		file_loc = cwd + '/' + file
		output = []
		header = '### ' + file
		contents_header = '**contents of %s**' % (file)
		warnings_header = '**warnings about %s**' % (file)
		results_header = '**results of %s**' % (file)

		output.append(header)
		file_contents = run(['cat', file], status=False)
		output.extend([contents_header, indent4(file_contents)])

		# wrapping the possible list in list() will always return a list
		# but doesn't return an extra-nested list
		steps = flatten([spec['files'][file]])
		for step in steps:
			# if step:
			command = step.replace('$@', file)
			status, compilation = run(command.split())
			output.extend([warnings_header, "`%s`" % command, indent4(compilation)])

		inputs = spec.get('inputs', {})
		tests = flatten([spec['tests'][file]])
		for test in tests:
			test = test.replace('$@', file)
			if os.path.exists(file_loc):
				if any([input in test for input in inputs]):
					output.append(results_header)
					for input, contents in inputs.items():
						status, result = run_file(file_loc + '.exec', input=contents)
						output.extend(["`%s`" % test, indent4(result)])
				else:
					status, result = run_file(file_loc + '.exec')
					output.extend([results_header, indent4(result)])
			else:
				output.extend([results_header, 'File %s could not be found to run.' % file])

		results.append('\n\n'.join(output))

	[run(['rm', '-f', file + '.exec']) for file in spec['files']]
	[os.remove(cwd + '/' + input) for input in spec.get('inputs', {})]

	return '# %s — %s \n %s' % (
		hw_number,
		username,
		'\n'.join(results))


if __name__ == '__main__':
	hw = sys.argv[1]
	user = sys.argv[2]
	print(markdownify(hw, user))
