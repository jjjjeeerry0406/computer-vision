import numpy as np
a=np.array([[1,4],[2,5],[3,6]])
b=a[:2, :]
#print(b)
c=a[2, :]
#print(c)
#print(b/c)
d=np.ones((2,a.shape[1]))
print(d)