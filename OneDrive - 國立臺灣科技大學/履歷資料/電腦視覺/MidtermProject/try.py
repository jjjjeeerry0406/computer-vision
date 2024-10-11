import numpy as np

  # 创建一个空列表

arr1 = [[1, 2],[3,4],[5,6]]
arr2 = [3, 4]
arr3 = [10,9]
arr_list = [arr3,]
# 使用 append 方法将数组添加到列表中
#arr_list.append(arr1[0])
#arr_list.append(arr2)


for i in range(3):
    arr_list.append(arr1[i])
# 将列表转换为数组的数组
merged_arr = [arr1,arr2]
np.savetxt('arr_list.xyz',arr_list)
print(arr_list)
