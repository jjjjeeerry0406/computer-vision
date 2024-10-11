import numpy as np
from PIL import Image, ImageDraw

# read image1
image1 = Image.open("SceneFromCamera1.jpg")

# read image2
image2 = Image.open("SceneFromCamera2.jpg")


width, height = image2.size
#print(width,height)


#read the 3d points data file 
data=np.loadtxt('3D_Trajectory.xyz')

x = data[:, 0]  
y = data[:, 1]  
z = data[:, 2]
#print(x[1])

#cam1
# 相機内部參數
K1 = np.array([[2666.6667,0.,960.],
              [0.,2666.6667,540.],
              [0.,0.,1.]])
#外部參數（旋轉和平移矩陣）
RT1 = np.array([[0.9874449,-0.1576334,-0.0102154,11.840861],
              [-0.0165432 , -0.0388828 , -0.9991068  , 1.1459197],
              [0.1570954 ,  0.986732 ,  -0.0410024  , 50.106411]])

#cam2
# 相機内部參數
K2 = np.array([[4266.667 ,  0. , 960.],
              [0.,  4266.667, 540.],
              [0.,0.,1.]])
#外部參數（旋轉和平移矩陣）
RT2 = np.array([[-0.0000004 , -1.      ,    0.0000001  , 12.915463],
              [ -0.299365  ,  0.0  ,-0.9541386 , -7.8007503],
              [0.9541386 , -0.0000004  ,-0.299365  ,  116.06975 ]])

#X：world coordinate
X3d = np.array([x,y,z])
#print("X3d shape:", X3d[0][0])

# 齊次坐標
X3d_homogeneous = np.vstack((X3d, np.ones((1, X3d.shape[1]))))
#print("x3d",X3d.shape[1])
#print("x3d_h",X3d_homogeneous)
# x=K[RT]X
x2d_cam1 = np.dot(np.dot(K1, RT1), X3d_homogeneous)
x2d_cam2 = np.dot(np.dot(K2, RT2), X3d_homogeneous)
print(x2d_cam1)
#print(np.dot(K1, RT1).shape)
#print(X3d_homogeneous.shape)
# 三維坐標轉化成二維
x2d_cam1 = x2d_cam1[:2, :] / x2d_cam1[2, :]
x2d_cam2 = x2d_cam2[:2, :] / x2d_cam2[2, :]
#print(x2d_cam1)



pixel_x_cam1 = x2d_cam1[0] #cam1的image的x坐標
pixel_y_cam1 = x2d_cam1[1] #cam1的image的y坐標
pixel_x_cam2 = x2d_cam2[0] #cam2的image的x坐標
pixel_y_cam2 = x2d_cam2[1] #cam2的image的y坐標


draw = ImageDraw.Draw(image1)
for x1, y1, x2, y2 in zip(pixel_x_cam1[:-1], pixel_y_cam1[:-1], pixel_x_cam1[1:], pixel_y_cam1[1:]):
    draw.line((x1, y1, x2, y2), fill='black', width=2,joint='curve')

draw = ImageDraw.Draw(image2)
for x1, y1, x2, y2 in zip(pixel_x_cam2[:-1], pixel_y_cam2[:-1], pixel_x_cam2[1:], pixel_y_cam2[1:]):
    draw.line((x1, y1, x2, y2), fill='black', width=2,joint='curve')

# 顯示圖像
#image1.show()
#image2.show()
