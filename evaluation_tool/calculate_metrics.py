
import numpy as np
import argparse
from tqdm import tqdm
import os
from PIL import Image
import torchvision.transforms as transforms
from saliency_metric import cal_mae,cal_fm,cal_sm,cal_em,cal_wfm


class test_dataset:
    def __init__(self, image_root, gt_root):
        self.img_list = [os.path.splitext(f)[0] for f in os.listdir(gt_root) if f.endswith('.png')]
        self.image_root = image_root
        self.gt_root = gt_root
        self.transform = transforms.Compose([
            transforms.ToTensor(),
        ])
        self.gt_transform = transforms.ToTensor()
        self.size = len(self.img_list)
        self.index = 0

    def load_data(self):
        #根据不同论文，需要修改图片命名格式
        image = self.binary_loader(os.path.join(self.image_root,self.img_list[self.index]+ '.png'))
        #测试集所有mask都是png格式
        gt = self.binary_loader(os.path.join(self.gt_root,self.img_list[self.index] + '.png'))
        self.index += 1
        return image, gt

    def binary_loader(self, path):
        with open(path, 'rb') as f:
            img = Image.open(f)
            return img.convert('L')

def evaluate_metrics(test_GT_Root, pred_salmap_root):
    #获取数据集名称
    dataset_name = test_GT_Root.split('/')[-1]
    #获取mask标签的路径
    mask_root = test_GT_Root + '/test_masks/'
    #加载数据集
    test_loader = test_dataset(pred_salmap_root, mask_root)
    #定义评价指标
    mae, fm, sm, em, wfm = cal_mae(), cal_fm(test_loader.size), cal_sm(), cal_em(), cal_wfm()
    for i in tqdm(range(test_loader.size)):
        sal, gt = test_loader.load_data()
        #尺寸不一致则修改尺寸
        if sal.size != gt.size:
            x, y = gt.size
            sal = sal.resize((x, y))
        gt = np.asarray(gt, np.float32)
        gt /= (gt.max() + 1e-8)
        gt[gt > 0.5] = 1
        gt[gt != 1] = 0
        res = sal
        res = np.array(res)
        if res.max() == res.min():
            res = res / 255
        else:
            res = (res - res.min()) / (res.max() - res.min())
        mae.update(res, gt)
        sm.update(res, gt)
        fm.update(res, gt)
        em.update(res, gt)
        wfm.update(res, gt)

    MAE = mae.show()
    maxf, meanf, _, _ = fm.show()
    sm = sm.show()
    em = em.show()
    wfm = wfm.show()
    print('\n{}:  MAE: {:.4f} maxF: {:.4f} avgF: {:.4f} wfm: {:.4f} Sm: {:.4f} Em: {:.4f}'
          .format(dataset_name, MAE, maxf,meanf, wfm, sm,em))

if __name__ == '__main__':
    """
        opt参数解析：
        GT-root:测试集的路径
        salmap_root:论文预测结果的路径
        cuda:是否使用GPU进行训练
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--GT-root', type=str, default='./test_dataset/', help='path to test data')
    parser.add_argument('--salmap-root', type=str, default='./Ours/', help='path to saliency map')
    parser.add_argument('--cuda', action='store_true', default=True, help='use cuda')
    args = parser.parse_args()

    #定义所有测试集
    GT_dataset = ['DUT-RGBD', 'NLPR', 'NJUD-485', 'NJUD-500', 'DES-RGBD135', 'STEREO-797', 'STEREO-1000', 'SSD', 'LFSD', 'SIP']
    #选择要计算评价指标的数据集
    test_data = ['DUT-RGBD', 'NLPR', 'NJUD-500', 'DES-RGBD135', 'STEREO-797', 'SSD', 'LFSD', 'SIP']

    for test_name in test_data:
        test_GT_Root = os.path.join(args.GT_root + test_name)
        pred_salmap_root = os.path.join(args.salmap_root + test_name)
        #计算评价指标
        evaluate_metrics(test_GT_Root, pred_salmap_root)


