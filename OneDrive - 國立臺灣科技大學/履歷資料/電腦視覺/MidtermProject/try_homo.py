import numpy as np
from scipy.linalg import svd
import cv2
# Define matrices A and B
a = np.array([[292, 168], [558, 92], [560, 937], [309, 729]], dtype=np.float32)
b = np.array([[-100, 100], [100, 100], [100, -100], [-100, -100]], dtype=np.float32)

M= cv2.findHomography(a,b)


ans=[]
ans=[M[0]]
print(ans)
arr=np.array([292, 168,1])
anss=np.dot(ans,arr)
print(anss)
print(anss/2.2393011158)
