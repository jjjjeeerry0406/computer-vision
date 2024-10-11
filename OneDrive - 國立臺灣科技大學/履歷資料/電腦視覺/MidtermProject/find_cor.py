import cv2
import numpy as np
import open3d as o3d
import pandas as pd

def find_cor(img):
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

    return left_up[0], right_up[0], right_down[0], left_down[0]