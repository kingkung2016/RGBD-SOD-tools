
import os
import cv2
import numpy as np

def inverse(img_root,img_name):

    img=cv2.imread(os.path.join(img_root,img_name))
    #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #归一化
    #img_norm = numpy.zeros(img_gray.shape)
    #cv2.normalize(img_read, img_norm, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    #imcomplement函数的实现
    table = np.array([255 - i for i in np.arange(0, 256)]).astype("uint8")
    result = cv2.LUT(img, table)
    result = np.array(result)

    return result

def load(data_name, dataset_path):
    #获取路径
    img_root = os.path.join(dataset_path, data_name, 'test_depth')
    file_names = os.listdir(img_root)

    #创建文件夹储存处理后图像
    inverse_dir = 'test_depth_inverse'
    url = os.path.join(dataset_path, data_name, inverse_dir)
    if not os.path.exists(url):
        os.mkdir(url)

    #处理图片
    for i, name in enumerate(file_names):
        temp = inverse(img_root, name)
        save_path = os.path.join(url, name)
        cv2.imwrite(save_path, temp)


if __name__ == '__main__':
    dataset_path = 'G:/dataset/RGB-D/test_dataset/'
    #写入所有测试集
    dataset = ['DUT-RGBD', 'NLPR', 'NJUD-485', 'NJUD-500', 'DES-RGBD135', 'STEREO-797', 'STEREO-1000', 'SSD', 'LFSD', 'SIP']
    #选择要处理的数据集
    handle_data = ['DES-RGBD135', 'LFSD', 'NJUD-500', 'SSD', 'STEREO-797']
    for data_name in handle_data:
        load(data_name, dataset_path)
