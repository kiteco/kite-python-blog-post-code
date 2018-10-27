# Add two matrices of size 2x3 using Pytorch
import torch

a = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
a = torch.Tensor(a)
b = a[0] + a[1]
print("sum of the two matrices of the 2-D tensor:", b)
