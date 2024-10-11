import numpy as np
import matplotlib.pyplot as plt

#載入相片及讀取xyz數值
img1 = plt.imread('C:/Users/User/OneDrive - 國立臺灣科技大學/履歷資料/電腦視覺/HW1/SceneFromCamera1.jpg')
img2 = plt.imread('C:/Users/User/OneDrive - 國立臺灣科技大學/履歷資料/電腦視覺/HW1/SceneFromCamera2.jpg')
data=np.loadtxt('C:/Users/User/OneDrive - 國立臺灣科技大學/履歷資料/電腦視覺/HW1/3D_Trajectory.xyz')


#定義相機參數
Cam1_K =np.array([
[2666.6667      ,0.        ,960.],
[0.             ,2666.6667 ,540.],
[0.             ,0.        ,1.  ]])
#print(Cam1_K[1][1])

Cam1_RT=np.array([
[0.9874449      ,-0.1576334    ,-0.0102154   ,11.840861],
[-0.0165432     ,-0.0388828    ,-0.9991068   ,1.1459197],
[ 0.1570954     ,0.986732      ,-0.0410024   ,50.106411]  ])


Cam2_K=np.array([
[4266.667  ,0.         ,960.],
[0         ,4266.667   ,540.],
[0.        ,0.         ,1. ] ])

Cam2_RT=np.array([
[-0.0000004     ,-1.        ,0.0000001  ,12.915463],
[-0.299365      ,0.0        ,-0.9541386 ,-7.8007503],
[ 0.9541386     ,-0.0000004 ,-0.299365  ,116.06975 ] ])

#create 3D array 
x_3d=np.array([data[:,0],data[:,1],data[:,2]])

#Homogenous 3D vector
fx=1     #focal length ,lecture2 p32
fy=1
Extri_Para=np.dot(([fx,0,0],[0,fy,0],[0,0,1]),x_3d)
Homo_3D=np.vstack([Extri_Para,np.ones((1 ,Extri_Para.shape[1])) ])

#X_2D=Cam_K*am_R|T*X_3D
x_2d=np.dot(np.dot(Cam1_K, Cam1_RT), Homo_3D)
y_2d=np.dot(np.dot(Cam2_K, Cam2_RT), Homo_3D)
#print(x_2d)

#Transform 3D coordinate to 2D 
cam1_2d = x_2d[:2, :]/x_2d[2, :]
cam2_2d = y_2d[:2, :]/y_2d[2, :]

#define line coordinate
line_x_1=cam1_2d[0]
line_y_1=cam1_2d[1]
line_x_2=cam2_2d[0]
line_y_2=cam2_2d[1]

#image1
plt.figure()#設定多開視窗
plt.plot(line_x_1,line_y_1)#draw line
plt.xticks([]) # remove x-axis
plt.yticks([]) # remove y-axis
plt.imshow(img1)
plt.savefig("M11225007_1.jpg")#save image1 

#image2
plt.figure()#設定多開視窗
plt.plot(line_x_2,line_y_2)#draw line
plt.xticks([]) # remove x-axis
plt.yticks([]) # remove y-axis
plt.imshow(img2)
plt.savefig("M11225007_2.jpg")#save image2       

#show result
plt.show()
