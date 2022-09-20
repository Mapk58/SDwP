from math import factorial
from task1 import decorator_1
from task2 import decorator_2 
from task3 import decorator_3 
from task4 import decorator_4 

def t3_printer(table):
    qwe = table[:]
    qwe.sort(key = lambda x: x[1])
    print('PROGRAM | RANK | TIME ELAPSED')
    for i in range(len(qwe)):
        print(f'{qwe[i][0]}\t {i+1}\t{qwe[i][1]}')

@decorator_1
def f1(arlen=1000):
    """
    This function calculates squares
    :param arlen: length of array
    """ 
    arr = [i for i in range(arlen)]
    arr2 = []
    l = lambda x: x**2
    for i in arr:
        arr2.append(l(i))
    print(arr2)
    
@decorator_1
def f2(arlen=10000):
    """
    This function calculates cubes
    :param arlen: length of array
    """ 
    arr = [i for i in range(arlen)]
    arr2 = []
    l = lambda x: x**3
    for i in arr:
        arr2.append(l(i))
    print(arr2)

@decorator_1
def f3(x=10,y=20,z=30):
    """
    This function solves quadratic equation
    :param x: first coefficient
    :param y: second coefficient
    :param z: third coefficient
    """
    d = (y**2) - (4*x*z)
    s1 = (-y-(d**(0.5)))/(2*x)
    s2 = (-y+(d**(0.5)))/(2*x)
    print(s1, s2)

@decorator_1
def f4(n=3):
    """
    This function prints Pascal triangle
    :param n: number of lines
    """
    for i in range(n):
        for j in range(n-i+1):
            print(end=" ")
        for j in range(i+1):
            print(factorial(i)//(factorial(j)*factorial(i-j)), end=" ")
        print()

@decorator_4
def f5():
    print(1/0)

if __name__ == '__main__':
    f1()
    f2()
    f3()
    f4()
    
    ## Uncomment next line to test task_3:
    # t3_printer(decorator_3.table)

    ## Uncomment next line to test task_4:
    # f5()
