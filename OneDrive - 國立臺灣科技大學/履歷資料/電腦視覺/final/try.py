import cv2
import numpy as np
import function as fun


directory_path =  'C:/Users/User/Desktop/電腦視覺/FinalProject/SBS images'
file_extension = '.jpg'
file_num= fun.count_files_in_directory(directory_path, file_extension)#計算jpg格式檔案數量

img = []
for i in range(file_num):
    image = cv2.imread(f'SBS images/{i:03d}.jpg')
    img.append(image)
img_color=cv2.imread('SBS images/000.jpg')
point_lft = []        
point_rgt = []

target_coord = {
    'left_hat': ((180, 52), (400, 320)),
    'right_hat': ((963, 6), (1206, 290)),
    'left_body': ((160, 350), (507, 600)),
    'right_body': ((925, 320), (1280, 590)),
    'left_foot': ((232, 600), (500, 850)),
    'right_foot': ((961, 590), (1280, 875))
}
for _,image in enumerate(img):
    left_pt, right_pt = fun.find_blue(image, 720, target_coord, 25)#get blue point on image
    point_lft.append(left_pt)
    point_rgt.append(right_pt)
k1 = np.array([[1000.0, 0.0, 360.0],
                [0.0, 1000.0, 640.0],
                [0.0, 0.0, 1.0]])

rt1 = np.array([[0.88649035, -0.46274707, -0.00, -14.42428],
                [-0.070794605, -0.13562201, -0.98822814, 86.532959],
                [0.45729965, 0.8760547, -0.1529876, 235.35446]])

k2 = np.array([[1100.0, 0.0, 360.0],
                [0.0, 1100.0, 640.0],
                [0.0, 0.0, 1.0]])

rt2 = np.array([[0.98480779, -0.17364818, -4.9342116E-8, -0.98420829],
                [-0.026566068, -0.15066338, -0.98822814, 85.070221],
                [0.17160401, 0.97321475, -0.1529876, 236.97873]])

F = np.array([[3.283965767647195E-7, -6.76098398189792E-6, 0.0021123144539793737],
              [-8.046341661808292E-6, 3.05632173594769E-8, 0.05124913199417346],
              [0.0048160232373805345, -0.051062699158041805, 1.0706286680443888]])

P = np.dot(k1, rt1)
Pp = np.dot(k2, rt2)
p3d=[]

for i in range(file_num):
    for left_pt in point_lft[i]:
        left_pt = np.array([left_pt[0], left_pt[1], 1])
        epi=fun.epi_polar_line(F,left_pt)#calculate epipolar line
        min_dist = 150    
        u, v = left_pt[0], left_pt[1]           
        up=None
        vp=None
        for right_pt in point_rgt[i]:
            right_pt = np.array([right_pt[0]-720, right_pt[1], 1])    
            dist = abs(np.dot(right_pt, epi))
            if dist < min_dist:
                min_dist = dist
                up=right_pt[0]
                vp=right_pt[1]
        if up == None or vp == None :#if can't find correct corresponding point, then skip 
            continue 
        pt_3d,A=fun.direct_triangle(k1,rt1,k2,rt2,u,v,up,vp)#calculate 3D point by direct tringle method
        check_pt = np.dot(A, pt_3d)
        check_pt = [x**2 for x in check_pt]
        error_pt = sum(check_pt) ** 0.5
        if error_pt < 10:
            r, g, b = image[v, u][2], image[v, u][1], image[v, u][0]
            numm=[pt_3d[0],pt_3d[1],pt_3d[2],r,g,b]
            p3d.append(numm)

np.savetxt('m11225007.txt',p3d)