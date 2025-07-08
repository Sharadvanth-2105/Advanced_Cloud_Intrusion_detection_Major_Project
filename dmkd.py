#program to append data vertically and horizantally using numpy
 
import numpy as np
mat_a=np.array([[1,2,3],[4,5,6]])
mat_b=np.array([[7,8,9],[10,11,12]])
h_stack=np.hstack(mat_a)
v_stack=np.vstack(mat_b)
print(h_stack)
print(v_stack)

