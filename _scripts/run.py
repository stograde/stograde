import subprocess

def run(*args, **kwargs):
	if ('input' in kwargs) and (type(kwargs['input']) is not bytes):
		kwargs['input'] = bytes(kwargs['input'], encoding='utf-8')

	byte_content = subprocess.check_output(*args, **kwargs)
	return bytes.decode(byte_content, encoding='utf-8')
