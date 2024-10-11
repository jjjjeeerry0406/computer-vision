import numpy as np
import function as fun

x = [[8,0,6],#選擇3D點
     [0,0,6],
     [0,6,6],
     [8,6,6],
     [8,0,6],
     [8,6,6],
     [8,6,0],
     [8,0,0],
     [8,6,6],
     [0,6,6],
     [0,6,0],
     [8,6,0]]

uv=[[357,161],#對應的UV座標
    [1050,57],
    [1440,176],
    [630,351],
    [357,161],
    [630,351],
    [685,1023],
    [435,708],
    [630,351],
    [1440,176],
    [1376,739],
    [685,1023]]
p=fun.determin_puv(x,uv)#求出puv矩陣
#print('p',p)
k,rt=fun.project_reconstru_matrix(np.array(p))#求出k及rt矩陣
print('k',k)
print('rt',rt)
r = rt[:3, :3]
t = rt[:, -1]
camera_pos=fun.camera_pos(r,t)#求出相機位置
print('camera position',camera_pos)
