from time import time
import contextlib
import io

def decorator_1(f):
    def qwe(*args, **kwargs):
        time1 = time()
        with contextlib.redirect_stdout(io.StringIO()) as file:
            f(*args, **kwargs)
        # f(*args)
        time2 = time()
        qwe.count += 1
        print(f'{f.__name__} call {qwe.count} executed in {time2-time1} sec')
        
    qwe.count = 0
    return qwe