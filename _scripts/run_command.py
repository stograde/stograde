import sys
import subprocess

def run(*args, status=True, **kwargs):
	try:
		result = (0, subprocess.check_output(
			*args,
			stderr=subprocess.STDOUT,
			universal_newlines=True,
			**kwargs))
	except subprocess.CalledProcessError as err:
		result = (1, err.output)
	except subprocess.TimeoutExpired as err:
		result = (1, err.output)
	except FileNotFoundError as err:
		result = (1, repr(err))
	except ProcessLookupError as err:
		result = (1, repr(err))

	# print(result)

	return result if status else result[1]
