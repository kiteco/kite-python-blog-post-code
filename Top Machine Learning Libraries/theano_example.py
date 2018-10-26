import theano
from theano import tensor

# declare two floating point scalars as a and b
a = tensor.dscalar()
b = tensor.dscalar()

# create a simple expression of multiplication
c = a * b

# convert the expression into an object that takes a and b as input
# and calculates a value for c
f = theano.function([a, b], c)

# bind 1.5 to 'a', 2.5 to 'b', and evaluate 'c'
# assert if the function, f predicts the right answer when 1.5 and 2.5 are multiplied
assert 3.75 == f(1.5, 2.5)
