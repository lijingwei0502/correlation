import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir(os.path.dirname(os.getcwd()))
nets = ['Resnet18','EfficientNetB0', 'SENet18']
# 读取数据


x = []
y = []
for net in nets:
    root = 'final/' + str(net) + '.txt'
    data = np.genfromtxt(root)
    if net == 'EfficientNetB0':
        data = data[:72]

    # 打印原始数据的行数
    print("原始数据的行数:", data.shape[0])

    # 定义 structured array 的 dtype
    dtype = [('col' + str(i), float) for i in range(data.shape[1])]

    # 将数据转换为 structured array
    structured_data = np.core.records.fromarrays(data.T, dtype=dtype)

    # 根据最后三列排序
    sorted_data = np.sort(structured_data, order=['col23', 'col24', 'col25'])

    # 使用 numpy 的 split 函数根据最后三列分组
    unique_keys, indices = np.unique(sorted_data[['col23', 'col24', 'col25']], return_index=True, axis=0)
    grouped_data = np.split(sorted_data, indices[1:])

    # 对每个组进行平均
    averaged_data = []
    for group in grouped_data:
        # 将每个分组转换为普通的 NumPy 数组
        group_array = np.array(group.tolist())
        averaged_data.append(group_array.mean(axis=0))

    averaged_data = np.array(averaged_data)
    # 打印处理后数据的行数
    print("处理后数据的行数:", averaged_data.shape[0])

    #indexs = [1,5,10,15,20]
    indexs = [20]
    # 为每个 epoch 值绘制并保存一张散点图
    for index in indexs:
        # 过滤出当前 epoch 的数据
        x_current = averaged_data[:, index]
        #y_current = averaged_data[:, 21]-averaged_data[:, 22]
        y_current = averaged_data[:,22]
        x.append(x_current)
        y.append(y_current)


# Setting the figure size to match the uploaded image's aspect ratio
plt.figure(figsize=(10, 8))

# Plotting the data
plt.scatter(x[0], y[0], label='Resnet18', color='blue', marker='o')
plt.scatter(x[1], y[1], label='EfficientNetB0', color='red', marker='v')
plt.scatter(x[2], y[2], label='SENet18', color='black', marker='^')

# Adjusting font sizes to match the uploaded image as closely as possible
plt.title('Average Regions vs. Test Accuracy', fontsize=18)
plt.xlabel('Average regions', fontsize=16)
plt.ylabel('Test Accuracy', fontsize=16)
plt.legend(fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=14)

if os.path.exists('final_corr') == False:
    os.mkdir('final_corr')
root = 'final_corr' + '/' + 'start.png'
plt.savefig(root)  # 保存图像

