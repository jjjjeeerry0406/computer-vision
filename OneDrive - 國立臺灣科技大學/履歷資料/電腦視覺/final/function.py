import cv2
import numpy as np
import pandas as pd
import os
from scipy.linalg import svd

def count_files_in_directory(directory, file_extension):
    if not os.path.isdir(directory):
        raise ValueError(f"The directory {directory} does not exist")
    file_count = len([f for f in os.listdir(directory) if f.endswith(file_extension) and os.path.isfile(os.path.join(directory, f))])
    return file_count

def direct_triangle(k1,rt1,k2,rt2,u,v,up,vp):
    #define [k|rt]
    P = np.dot(k1, rt1)
    Pp = np.dot(k2, rt2)

    p1 = P[0, :]
    p2 = P[1, :]
    p3 = P[2, :]
    pp1 = Pp[0, :]
    pp2 = Pp[1, :]
    pp3 = Pp[2, :]
    # define matrix A
    A = np.vstack([
        u * p3 - p1,
        v * p3 - p2,
        up * pp3 - pp1,
        vp * pp3 - pp2
    ])

    # using SVD to get the answer
    U, S, Vt = svd(A)
    V = Vt.T
    point_3D=V[:,3]/ V[-1][-1]#calculate 3D point by normalization
    return point_3D,A

def epi_polar_line(F,x):
    epi_parameter= np.dot(F, x)
    return epi_parameter

def blue_hp(pixel):
    return (10 < pixel[0] < 20 and pixel[1] < 15 and 20 < pixel[2] < 50)

def check_pixel(x, y, box):
    return box[0][0] < x < box[1][0] and box[0][1] < y < box[1][1]

def fill_pt(points, mean, min, max):
    return [pt for pt in points if min < pt[0] - mean < max]

def find_blue(image, midX, target_coord, blue_thres):
    left_pt, right_pt = [], []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            pixel = image[y, x]
            if x < midX:
                if (check_pixel(x, y, target_coord['left_hat']) and (blue_hp(pixel) or check_blue(pixel, blue_thres)) or
                    check_pixel(x, y, target_coord['left_foot']) and check_blue(pixel, blue_thres) or
                    check_pixel(x, y, target_coord['left_body']) and check_blue(pixel, blue_thres)):
                    left_pt.append([x, y])
            else:
                if (check_pixel(x, y, target_coord['right_hat']) and (blue_hp(pixel) or check_blue(pixel, blue_thres)) or
                    check_pixel(x, y, target_coord['right_foot']) and check_blue(pixel, blue_thres) or
                    check_pixel(x, y, target_coord['right_body']) and check_blue(pixel, blue_thres)):
                    right_pt.append([x, y])

    left_pts = fill_pt(left_pt, np.mean([pt[0] for pt in left_pt]), -50, 100)
    right_pts = fill_pt(right_pt, np.mean([pt[0] for pt in right_pt]), -30, 60)

    return left_pts, right_pts
def check_blue(pixel, blue_thres):
    return (pixel[0] > pixel[1] + blue_thres and pixel[0] > pixel[2] + blue_thres)
