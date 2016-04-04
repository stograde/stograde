def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.__has_run:
            wrapper.__has_run = True
            return f(*args, **kwargs)
    wrapper.__has_run = False
    return wrapper
