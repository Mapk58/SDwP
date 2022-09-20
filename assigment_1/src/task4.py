from time import time
import contextlib
import io
from task3 import decorator_3

class decorator_4:

    def __init__(self, f):
        self.name = f.__name__
        self.f = decorator_3(f)

    def __call__(self, *args, **kwargs):
        try:
            self.f(*args, **kwargs)
        except Exception as e:
            file = open('task4.txt', mode='a')
            file.write(f'Timestamp: {time()},\nError: {e}\n\n')
            file.close()