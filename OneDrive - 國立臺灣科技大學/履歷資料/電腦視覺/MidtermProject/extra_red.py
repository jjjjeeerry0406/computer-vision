import cv2
import numpy as np
import open3d as o3d
import pandas as pd


def find_red(img):
    # transform image's RGB into HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # get red region
    mask = cv2.inRange(hsv_img, (0, 43, 46), (10, 255, 255))

    # add amsk on original image
    masked_img = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=mask)

    # show mask image
    #cv2.imshow('img', img)
    #cv2.imshow('masked img', mask)

    cv2.waitKey(0)
    #cv2.imwrite("mask.jpg",masked_img)
    width= masked_img.shape[0]
    heigh= masked_img.shape[1]
    #np_arr=np.array
    num=0
    num1=0
    lt=[]
    lt1=[]

    #find red
    for x in range(width):
        for y in range(heigh):
            if masked_img[y][x][2]!=0:#RGB index, Green and Blue isn't equal to 0(not black)
                lt.append([x,y])#red point coordinate
                lt1.append([x,y,1])
                num+=1
            if masked_img[y][x][2]==0:#rgb中b和g不等於0(不是黑色)
                num1+=1

    

    #collect all x-value
    val=np.array(lt)

    tem_val=[]
    for m in range(len(val)):
        tem_val.append(lt[m][0])
    x_val=np.array(tem_val)
    #print(x_val)

    #collect all y-value
    tem_val=[]
    for m in range(len(val)):
        tem_val.append(lt[m][1])
    y_val=np.array(tem_val)
    #print(y_val)

    #find custom coordinates
    x_coor=(x_val.max()+x_val.min())/2
    y_coor=(y_val.max()+y_val.min())/2
    print(x_coor)
    print(y_coor)
    #find four corner
    left_up=[]
    right_up=[]
    left_down=[]
    right_down=[]

    #find left up corner
    for k in range(len(val)):
        if lt[k][0]<x_coor and lt[k][1]<y_coor:
            left_up.append(lt[k])


    #find left down corner
    for k in range(len(val)):
        if lt[k][0]<x_coor and lt[k][1]>y_coor:
            left_down.append(lt[k])
    #print(left_down)

    #find right up corner
    for k in range(len(val)):
        if lt[k][0]>x_coor and lt[k][1]<y_coor:
            right_up.append(lt[k])
    #print(right_up)

    #find right down corner
    for k in range(len(val)):
        if lt[k][0]>x_coor and lt[k][1]>y_coor:
            right_down.append(lt[k])
    #print(right_down)
    #print(left_up[0],right_up[0],right_down[0],left_down[0])
    #calculate homo
    print(left_up[0], right_up[len(right_up)-1], right_down[len(right_down)-1], left_down[0])
    A = np.array([left_up[0], right_up[len(right_up)-1], right_down[len(right_down)-1], left_down[0]], dtype=np.float32)
    B = np.array([[100, 100], [-100, 100], [-100, -100], [100, -100]], dtype=np.float32)
    M=cv2.findHomography(A,B)
    mmm=[[-M[0][0][0],-M[0][0][1],-M[0][0][2]],
         [-M[0][1][0],-M[0][1][1],-M[0][1][2]],
         [ M[0][2][0], M[0][2][1], M[0][2][2]]]
    #print(lt)
    return mmm, lt

#img = cv2.imread('ShadowStrip/0022.jpg')
#m,lt=find_red(img)
#print('lt   ',lt)

images = [[],]


z=-26
xyz_points=[]
for i in range(55):
    image = cv2.imread(f'ShadowStrip/{i:04d}.jpg')
    m,lt=find_red(image)
    #images.append(lt)
#print("images   ",images[1])
#image = cv2.imread('ShadowStrip/0001.jpg')
#images.append(image)
#print(m)
    for pt in lt:
        pt.append(1)
        #print('PT1',pt)
        pt = np.dot(m, np.array(pt))
        #print('PT2',pt)
        pt = pt/pt[2]
        pt[-1] = z
        xyz_points.append(pt)
    z+=1 
with open('points4.xyz', 'w') as f:
    for pd in xyz_points:
        x, y, z = pd[0], pd[1], pd[2]
        f.write(f'{z} {-x} {-y}\n')     # 注意座標軸轉換