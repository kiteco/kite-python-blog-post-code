# Add two matrices of size 2x3 using Pytorch
import torch
a=[[1.,2.,3.],[4.,5.,6.]]
a=torch.Tensor(a)
b=a[0]+a[1]
print("sum of the two matrices of the 2-D tensor:",b)