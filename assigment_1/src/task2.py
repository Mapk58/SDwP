from time import time
import contextlib
import io
import inspect

def fprint(name, value):
    a = str(value).replace('\n', '\n\t')
    print(f'{name}:\t{a}')


def decorator_2(f):
    def qwe(*args, **kwargs):
        time1 = time()
        with contextlib.redirect_stdout(io.StringIO()) as file:
            f(*args, **kwargs)
        # f(*args)
        time2 = time()
        qwe.count += 1
        print(f'func call {qwe.count} executed in {time2-time1} sec')
        fprint('Name', f.__name__)
        fprint('Type', type(f))
        fprint('Sign', inspect.signature(f))
        fprint('Args', 'positional '+str(args)+'\nkeyworded '+str(kwargs))
        print('\n')
        fprint('Doc', inspect.getdoc(f))
        print('\n')
        fprint('Source', inspect.getsource(f))
        fprint('Output', file.getvalue())
        
    qwe.count = 0
    return qwe