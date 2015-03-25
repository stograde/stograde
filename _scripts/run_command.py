import sys
import subprocess

def run(*args, **kwargs):
	if ('input' in kwargs) and (type(kwargs['input']) is not bytes):
		kwargs['input'] = bytes(kwargs['input'], encoding='utf-8')

	bytes_content = b''
	result = ''

	try:
		bytes_content = subprocess.check_output(*args, stderr=subprocess.STDOUT, **kwargs)
	except subprocess.CalledProcessError as err:
		bytes_content = err.output
	except subprocess.TimeoutExpired as err:
		bytes_content = err.output
	except FileNotFoundError as err:
		result = repr(err)

	result = bytes.decode(bytes_content, encoding='utf-8') if bytes_content else result

	return result
