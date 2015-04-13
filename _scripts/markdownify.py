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

		output.extend([header, '\n'])
		file_status, file_contents = run(['cat', file])
		if file_status:
			output.append('**file %s does not exist**\n' % file)
			output.append('`ls .` says that these files exist:\n')
			output.append(indent4('\n'.join(os.listdir('.'))))
			results.append('\n'.join(output))
			continue

		output.extend(['**contents of %s**\n' % (file), indent4(file_contents)])
		output.append('\n')

		# wrapping the possible list in list() will always return a list
		# but doesn't return an extra-nested list
		steps = flatten([spec['files'][file]])
		any_step_failed = False
		for step in steps:
			command = step.replace('$@', file)
			status, compilation = run(command.split())
			if status:
				any_step_failed = True
				break

			if compilation:
				warnings_header = '**warnings: `%s`**' % (command)
				output.extend([warnings_header, indent4(compilation)])
			else:
				warnings_header = '**no warnings: `%s`**' % (command)
				output.extend([warnings_header])

			output.append('\n')

		if any_step_failed:
			continue


		inputs = spec.get('inputs', {})
		tests = flatten([spec['tests'][file]])
		for test in tests:
			test = test.replace('$@', file)
			output.append('**results of %s**\n' % (file))
			if os.path.exists(file_loc):
				if any([input in test for input in inputs]):
					for input, contents in inputs.items():
						status, result = run_file(file_loc + '.exec', input=contents)
						output.extend(["`%s`\n" % test, indent4(result)])
				else:
					status, result = run_file(file_loc + '.exec')
					output.extend(["`%s`\n" % test, indent4(result)])
			else:
				output.append('%s could not be found.\n' % file)

			output.append('\n')

		output.extend(["\n\n"])

		results.append('\n'.join(output))

	[run(['rm', '-f', file + '.exec']) for file in spec['files']]
	[os.remove(cwd + '/' + input) for input in spec.get('inputs', {})]

	return '# %s — %s \n%s' % (
		hw_number,
		username,
		''.join(results))


if __name__ == '__main__':
	hw = sys.argv[1]
	user = sys.argv[2]
	print(markdownify(hw, user))
