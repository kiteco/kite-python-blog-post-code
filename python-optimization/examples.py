# profiling
import cProfile


def fib(n):
    if n < 2:
        return 1
    return fib(n - 1) + fib(n - 2)


cProfile.run('fib(30)')

# basic timeit usage
import timeit

timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
timeit.timeit('"-".join([str(n) for n in range(100)])', number=10000)
timeit.timeit('"-".join(map(str, range(100)))', number=10000)

# creating a decorator
from timeit import default_timer


def timer(func):
    def wrapper(*args, **kwargs):
        begin = default_timer()
        result = func(*args, **kwargs)
        end = default_timer()
        print(f"{func.__name__} took {end - begin} seconds to compute.")
        return result

    return wrapper


@timer
def my_join():
    return "-".join(map(str, range(10000)))


my_join()

# Optimizing for speed
my_var = 'beautiful'

# slow
msg = 'hello ' + my_var + ' world'

# better
msg = 'hello %s world' % my_var

# even better:
msg = 'hello {} world'.format(my_var)

# best (and most Pythonic in Python 3)
msg = f'hello {my_var} world'

x = 1
y = 2

# Bad
temp = x
x = y
y = temp

# Good
x, y = y, x

# Bad
a = 42
x = a
y = a

# Good
a = 42
x = y = a


# New Fibonacci calculator
def fibon(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b


list(fibon(5))
