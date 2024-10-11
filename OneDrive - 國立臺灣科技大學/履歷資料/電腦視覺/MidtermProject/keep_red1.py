import cv2
import numpy as np
import open3d as o3d
import pandas as pd


def mid_project(img):
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

    np.savetxt('lt1.xyz',lt1)

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
    #print(right_down)
    print(left_up[0],right_up[0],right_down[0],left_down[0])
    #calculate homo
    A = np.array([left_up[0], right_up[0], right_down[0], left_down[0]], dtype=np.float32)
    B = np.array([[100, 100], [-100, 100], [-100, -100], [100, -100]], dtype=np.float32)
    M=cv2.findHomography(A,B)
    mmm=[[-M[0][0][0],-M[0][0][1],-M[0][0][2]],
         [-M[0][1][0],-M[0][1][1],-M[0][1][2]],
         [ M[0][2][0], M[0][2][1], M[0][2][2]]]


    #print(mmm)

    #inner product
    fp=[]
    #print(lt1)
    z=-27
    for i in range(len(lt1)):
        print('lt1',lt1[i])
        ans=np.dot(mmm,lt1[i])
        #print(ans[2])
        print(ans)
        ans=ans/ans[2]
        ans[-1] = z
        #print('ans',ans)
        
        final_p=np.array([ans[2],-ans[0],-ans[1]])
        fp.append(final_p)
    z+=1    
    xyz_points=[]
    for pt in lt:
        pt.append(1)
        print('PT1',pt)
        pt = np.dot(mmm, np.array(pt))
        print('PT2',pt)
        pt = pt/pt[2]
        pt[-1] = z
        xyz_points.append(pt)
    #show pcd
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(fp)
    pcd.paint_uniform_color([1, 0, 0])#set PCD into red color
    #o3d.visualization.draw_geometries([pcd])#visualization PCD
    
    np.array(fp).tolist()
    return xyz_points    #export final point in PCD



#img = cv2.imread('ShadowStrip/0001.jpg')
#fp=mid_project(img)


ddd=[]
#for i in range(55):
#    img = cv2.imread(f'ShadowStrip/{i:04d}.jpg')
#    fp=mid_project(img)
#    ddd.append(fp)
##np.savetxt('red1.xyz',ddd)
#print(ddd)

#print('ddd1',ddd)

img1 = cv2.imread('ShadowStrip/0001.jpg')
fp1=mid_project(img1)
#for jj in range(len(fp1)):
#    ddd.append(fp1[jj])
np.savetxt('red50.xyz',fp1)
#print('ddd2',ddd)

#for i in range(55):
#   img = cv2.imread(f'ShadowStrip/{i:04d}.jpg')
#   fp=mid_project(img)
#    for pp in fp:
#        x, y, z = pd[0], pd[1], pd[2]
#        np.savetxt('centers.xyz',pp)


