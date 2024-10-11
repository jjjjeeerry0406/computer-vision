#WARNING:code cost 3 hours to finish

from PIL import Image
import function as fun
import numpy as np

#step1 載入影像並裁除綠色部分
img = Image.open("Santa.jpg")
point=fun.img_get_pixel_color_and_position(img)#load image by PIL

#step2
uv = [[1414, 342],#uv座標
      [1420, 532],
      [1204, 844],
      [1441, 840],
      [1651, 856],
      [1309, 1254],
      [1560, 1260],
      [1297, 1620],
      [1564, 1621],
      [1432, 1422],
      [1246, 1416],
      [1639, 1431],
      [1434, 1522]]

x = [[0.301650, -5.007015, 60.261902],# 對應3D座標
     [0.110567, 2.662931, 51.900234],
     [10.846558, -2.108413, 37.410847],
     [-0.354580, 10.567294, 39.203934],
     [-10.326472, 0.208168, 36.743122],
     [7.138647, -7.378907, 12.298265],
     [-6.675469, -6.943602, 11.966425],
     [5.743905, 11.235051, 4.167382],
     [-6.016557, 10.601576, 4.020152],
     [0.041978, 15.007763, 14.732791],
     [9.962152, 10.816264, 14.359861],
     [-8.705679, 14.769521, 14.433470],
     [0.078845, 15.195429, 10.446424]]
p=fun.determin_puv(x,uv)#求PUV矩陣

#step 3
vertices = []   # x, y, z, nx, ny, nz
with open('Santa.xyz', 'r') as f:#讀取XYZ檔
    for line in f.readlines():
        vertices.append(list(map(float, line.split())))
#np.savetxt('vertices.txt',vertices)
front_point=[]
for i in range(len(vertices)):#選擇正面的3D點
    if vertices[i][4]>0:    
        #if vertices[i][4]>0.75:
        #    if vertices[i][1]>1:   
        front_point.append(vertices[i])
#np.savetxt('front_point.txt',front_point)#check front face
fin_ans=[]
print(vertices[0])
print(len(front_point))
print(len(point))

for i in range(len(front_point)):
    val=[front_point[i][0],front_point[i][1],front_point[i][2],1]
    tryr=np.dot(p,val)#將每個3D點乘上puv矩陣
    tryr=[tryr[0]/tryr[-1],tryr[1]/tryr[-1],tryr[2]/tryr[-1]]#正規化數值
    clo=fun.find_close_point(tryr,point)#找出接近的uv座標
    #print(clo[0][2])
    if len(clo)>0:#如果有找到相應的uv座標，儲存[x,y,z,nx,ny,nz,r,g,b,a]數據
        ans=[front_point[i][0],front_point[i][1]+1,front_point[i][2],front_point[i][3],front_point[i][4],front_point[0][5],clo[0][2],clo[0][3],clo[0][4],255]
        fin_ans.append(ans)
        
#step 4
np.savetxt('M11225007.txt',fin_ans)#數據轉存為txt


