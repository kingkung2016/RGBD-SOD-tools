import os
import cv2
import numpy as np

def sla2edge(img_root,img_name):

    img = cv2.imread(os.path.join(img_root,img_name), cv2.IMREAD_GRAYSCALE)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # gradient
    gradX = cv2.Sobel(img, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(img, ddepth=cv2.CV_32F, dx=0, dy=1)

    temp_edge = gradY * gradY + gradX * gradX

    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if temp_edge[x, y] != 0:
                temp_edge[x, y] = 255

    result = np.array(temp_edge, dtype='uint8')

    return result

def load(data_name, dataset_path):
    #获取路径
    img_root = os.path.join(dataset_path, data_name, 'train_masks')
    file_names = os.listdir(img_root)

    #创建文件夹储存处理后图像
    inverse_dir = 'train_edges'
    url = os.path.join(dataset_path, data_name, inverse_dir)
    if not os.path.exists(url):
        os.mkdir(url)

    #处理图片
    for i, name in enumerate(file_names):
        temp = sla2edge(img_root, name)
        save_path = os.path.join(url, name)
        cv2.imwrite(save_path, temp)


if __name__ == '__main__':
    dataset_path = 'G:/dataset/RGB-D/train_dataset/'
    #选择要处理的数据集
    handle_data = ['train_2185','train_2985']
    for data_name in handle_data:
        load(data_name, dataset_path)


