#function.py
import numpy as np
from scipy.linalg import qr, inv

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

def k_matrix(ha,hb,hc):

    # 轉置矩陣
    hap = ha.T
    hbp = hb.T
    hcp = hc.T
    # 創建矩陣 A
    A = np.array([[hap[0, 0]*hap[1, 0], hap[0, 0]*hap[1, 1]+hap[0, 1]*hap[1, 0], hap[0, 0]*hap[1, 2]+hap[0, 2]*hap[1, 0],
                   hap[0, 1]*hap[1, 1], hap[0, 1]*hap[1, 2]+hap[0, 2]*hap[1, 1], hap[0, 2]*hap[1, 2]],
                  [hap[0, 0]**2-hap[1, 0]**2, 2*(hap[0, 0]*hap[0, 1]-hap[1, 0]*hap[1, 1]), 2*(hap[0, 0]*hap[0, 2]-hap[1, 0]*hap[1, 2]),
                   hap[0, 1]**2-hap[1, 1]**2, 2*(hap[0, 1]*hap[0, 2]-hap[1, 1]*hap[1, 2]), hap[0, 2]**2-hap[1, 2]**2],
                  [hbp[0, 0]*hbp[1, 0], hbp[0, 0]*hbp[1, 1]+hbp[0, 1]*hbp[1, 0], hbp[0, 0]*hbp[1, 2]+hbp[0, 2]*hbp[1, 0],
                   hbp[0, 1]*hbp[1, 1], hbp[0, 1]*hbp[1, 2]+hbp[0, 2]*hbp[1, 1], hbp[0, 2]*hbp[1, 2]],
                  [hbp[0, 0]**2-hbp[1, 0]**2, 2*(hbp[0, 0]*hbp[0, 1]-hbp[1, 0]*hbp[1, 1]), 2*(hbp[0, 0]*hbp[0, 2]-hbp[1, 0]*hbp[1, 2]),
                   hbp[0, 1]**2-hbp[1, 1]**2, 2*(hbp[0, 1]*hbp[0, 2]-hbp[1, 1]*hbp[1, 2]), hbp[0, 2]**2-hbp[1, 2]**2],
                  [hcp[0, 0]*hcp[1, 0], hcp[0, 0]*hcp[1, 1]+hcp[0, 1]*hcp[1, 0], hcp[0, 0]*hcp[1, 2]+hcp[0, 2]*hcp[1, 0],
                   hcp[0, 1]*hcp[1, 1], hcp[0, 1]*hcp[1, 2]+hcp[0, 2]*hcp[1, 1], hcp[0, 2]*hcp[1, 2]],
                  [hcp[0, 0]**2-hcp[1, 0]**2, 2*(hcp[0, 0]*hcp[0, 1]-hcp[1, 0]*hcp[1, 1]), 2*(hcp[0, 0]*hcp[0, 2]-hcp[1, 0]*hcp[1, 2]),
                   hcp[0, 1]**2-hcp[1, 1]**2, 2*(hcp[0, 1]*hcp[0, 2]-hcp[1, 1]*hcp[1, 2]), hcp[0, 2]**2-hcp[1, 2]**2]])
    # 奇異值分解
    u, s, V = np.linalg.svd(A,True)
    # 構建 v 矩陣
    v = np.array([[V.T[0,5],V.T[1,5],V.T[2,5]],
                  [V.T[1,5],V.T[3,5],V.T[4,5]],
                 [V.T[2,5],V.T[4,5],V.T[5,5]]])
    # 反矩陣計算
    inv_v = inv(v)

    inv_v /= inv_v[2, 2]  # 將第三行第三列元素設置為1
    c = inv_v[0, 2]
    e = inv_v[1, 2]
    #print('inv_v[1, 1]',inv_v[1, 1])
    #print('e**2',e**2)
    d = np.sqrt(inv_v[1, 1]-e**2)
    
    b = (inv_v[0, 1]-c*e)/d
    a = np.sqrt(inv_v[0, 0]-b**2-c**2)
    # 創建 k 矩陣
    k = np.array([[a, b, c],
                  [0, d, e],
                  [0, 0, 1]])
    return k

def project_reconstru_matrix(P):

    Q, U = qr(inv(P[:3, :3]))#透過qr分解求出正交矩陣q及上三角矩陣u

    # 創建對角矩陣 d
    d = np.diag(np.sign(np.diag(U) * [-1] * len(U)))

    # 更新 Q 和 U
    Q = Q.dot(d)
    U = d.dot(U)

    # 計算行列式
    s = np.linalg.det(Q)

    # 計算 r 和 t
    r = s * Q.T
    t = s * U.dot(P[:3, 3])

    # 計算 k矩陣
    k = inv(U / U[2, 2])
    #計算rt矩陣
    rt=[[r[0][0],r[0][1],r[0][2],t[0]],
               [r[1][0],r[1][1],r[1][2],t[1]],
               [r[2][0],r[2][1],r[2][2],t[2]]]
    rt_martix=np.array(rt)
    return k,rt_martix

def rt_matrix(homo_matrix,k_matrix):
    ra = np.linalg.inv(k_matrix) @ homo_matrix
    r11 = np.sqrt(ra[0, 0]**2 + ra[1, 0]**2 + ra[2, 0]**2)
    r1 = ra[0:3, 0] / r11
    r12 = np.sqrt(ra[0, 1]**2 + ra[1, 1]**2 + ra[2, 1]**2)
    r2 = ra[0:3, 1] / r12
    r3 = np.cross(r1, r2)
    r4 = np.cross(r3, r1)
    t = (np.linalg.inv(k_matrix) @ homo_matrix[0:3, 2]) / 0.3206
    rt = np.column_stack((r1, r4, r3, t))
    #print(rt)
    return [r1, r4, r3],t,rt

def camera_pos(r_matrix, t_matrix):
    r_inv = np.linalg.inv(r_matrix)    # 求r矩陣的反矩陣
    camera_pos= -np.dot(r_inv, t_matrix)   # 計算相機三維位置
    return camera_pos