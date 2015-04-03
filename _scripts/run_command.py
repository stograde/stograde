from sys import stderr
import subprocess

def run(*args, status=True, **kwargs):
	# if ('input' in kwargs) and (type(kwargs['input']) is not bytes):
	# 	kwargs['input'] = bytes(kwargs['input'], encoding='utf-8')

	# bytes_content = b''
	# result = ''

	try:
		result = (0, subprocess.check_output(*args, stderr=subprocess.STDOUT, universal_newlines=True, **kwargs))
	except subprocess.CalledProcessError as err:
		result = (1, err.output)
	except subprocess.TimeoutExpired as err:
		result = (1, err.output)
	except FileNotFoundError as err:
		result = (1, repr(err))
	except UnicodeDecodeError as err:
		result = (1, repr(err))
	except Exception as err:
		# print(repr(err), file=stderr)
		result = (1, repr(err))

	# result = bytes.decode(bytes_content, encoding='utf-8') if bytes_content else result

	return result if status else result[1]
