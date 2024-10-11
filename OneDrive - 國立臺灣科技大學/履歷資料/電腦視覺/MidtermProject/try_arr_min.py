
import numpy as np
a = np.array([[1,5],[4,2]])
aaaa = np.array([[0,2],[2,5]])
aa=[]
b=[[1,5],[4,2]]
bb=[[0,2],[2,5]]
for i in range(2):
    
    aa.append(a[i][0])
bbb=list(zip(b,bb))
#bb.append(a)
print('bb1',bbb)
#bb.append(aaaa)
#print('bb2',bb)
aaa=np.array(aa)  
#print(aaa) 
#print(aaa[0].min().astype(int)) 
#print(a[0][0]) 
#if a[0][0]==aaa[0].min():
#    print(a[0])
#print(aaa[0].min())
#print(aaa[0].min())
#print(a[1])
dd=10
for k in range(2):

    #print(a[k-1][j-1])
    if a[k][0]>=aaa[0].min() and dd ==10:
        #print(a[0])
        print()
        #print(a[k])
#print(a.min()) #无参，所有中的最小值
#print(a.min(0)) # axis=0; 每列的最小值
#print(a.min(1)) # axis=1；每行的最小值
#print(a.max(0)) # axis=0; 每列的最小值
#print(a.max(1)) # axis=1；每行的最小值