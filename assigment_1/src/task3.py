from time import time
import contextlib
import io
from task2 import decorator_2

class decorator_3:
    
    table = []

    def __init__(self, f):
        self.name = f.__name__
        self.f = decorator_2(f)

    def __call__(self, *args, **kwargs):
        time1 = time()
        with contextlib.redirect_stdout(io.StringIO()) as file:
            self.f(*args, **kwargs)
        time2 = time()
        decorator_3.table.append([self.name, time2-time1])
        s = file.getvalue()
        file = open('task3.txt', mode='a')
        file.write(s)
        file.close()