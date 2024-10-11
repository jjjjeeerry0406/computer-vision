import cv2
import numpy as np

img = cv2.imread("Swap_ArtGallery.jpg")

src=np.array([[215,34], [798,104], [791,738], [225,800]])#定義相框位置
pts=np.array([[1223,142], [1450,140], [1440,405], [1220,396]])

M= cv2.findHomography(src, pts)#計算映射矩陣
HM1=np.array(M[0])
M_inv=np.linalg.inv(HM1)#計算逆映射矩陣  

result = cv2.warpPerspective(img, HM1, (img.shape[1], img.shape[0]))#影像映射
result1 = cv2.warpPerspective(img, M_inv, (img.shape[1], img.shape[0]))

mask1 = np.zeros_like(img)#定義遮罩大小    
mask2 = np.zeros_like(img)
cv2.fillConvexPoly(mask1, pts, (255, 255, 255))#將兩個相框位置塗成黑色，
cv2.fillConvexPoly(mask2, src, (255, 255, 255))

output = np.where(mask1 != 0, result, img)#若影像內有黑色區塊，則填入映射後的影像   
output = np.where(mask2 != 0, result1, output)

cv2.imwrite('m11225007.jpg', output )