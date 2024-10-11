import numpy as np
from PIL import Image
import math

def img_get_pixel_color_and_position(img):#裁掉圖片綠色部分
    rgb_data = img.convert("RGB")
    width, height = img.size

    lst=[]
    final=[]
    for y in range(height):
        for x in range(width):
            lst=[]
            r, g, b = rgb_data.getpixel((x, y))
            lst.extend([x,y,r,g,b])
            final.append(lst)
    #print(len(final))
    color_index=1.4
    color_project=[]
    for pd in final:
        x, y,r,g,b = pd[0], pd[1], pd[2],pd[3],pd[4]
        if 1132<=x<=1700 and 120<=y<=1700:#將圖片綠色部分裁掉，並儲存非綠色點的uv及rgb
            if g<=b*color_index or g<=r*color_index:
                lst=[x, y,r,g,b]
                color_project.append(lst)
    return color_project


def determin_puv(x,uv):#計算puv矩陣
    pp=[] 
    for i in range(len(x)):
        x[i].append(1)
        uv[i].append(1)
        p=[x[i][0],x[i][1],x[i][2],x[i][3],0,0,0,0,-uv[i][0]*x[i][0],-uv[i][0]*x[i][1],-uv[i][0]*x[i][2],-uv[i][0]*x[i][3]]
        pp.append(p)
        p=[0,0,0,0,x[i][0],x[i][1],x[i][2],x[i][3],-uv[i][1]*x[i][0],-uv[i][1]*x[i][1],-uv[i][1]*x[i][2],-uv[i][1]*x[i][3]]
        pp.append(p)
    pro=np.array(pp,dtype=np.float32)

    u,sigma,v=np.linalg.svd(pro)#用奇異值分解求puv矩陣
    pp=np.array(v[-1])
    pfin=[[pp[0]/pp[-1],pp[1]/pp[-1],pp[2]/pp[-1],pp[3]/pp[-1]],
          [pp[4]/pp[-1],pp[5]/pp[-1],pp[6]/pp[-1],pp[7]/pp[-1]],
          [pp[8]/pp[-1],pp[9]/pp[-1],pp[10]/pp[-1],pp[11]/pp[-1]]]
    return pfin

def find_close_point(target,uv):#由projection matrix計算出的uv座標，找出相應的rgb值
    close_num=[]
    for i in range(len(uv)):
        if math.isclose(target[0], uv[i][0],abs_tol=1):
            close_num.append(uv[i])

    close_num1=[]
    for i in range(len(close_num)):
        if math.isclose(target[1], close_num[i][1],abs_tol=1):
            close_num1.append(close_num[i])
    return close_num1
