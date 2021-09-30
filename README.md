README
===========================

Here is a project of RGB-D Saliency Object Detection, we will share the most common datasets, tools of calculating evaluation metrics, some skills of pre-trained and our new research advances...
****

## 目录
* [Datasets](#Datasets)
* [Evaluation tools](#Evaluation tools)
* [Pre-trained tools](#Pre-trained tools)
****

### Datasets
There are eight mainstream RGB-D saliency datasets:

|Dataset|DES/RGBD135|DUT-RGBD|LFSD|NJUD|NLPR|SIP|SSD|STEREO|
|---|---|---|---|---|---|---|---|---|
|Size|135|1200|100|2000|1000|929|80|1000/797|

- Tips: The authors of NJUD dataset published 2000 samples initially, but they updated them to 1985 samples subsequently.

#### There are two generally accepted settings of training datasets:
- Training dataset 1, including NJUD(1485) and NLPR(700), [fetch code is 2185](https://pan.baidu.com/s/17ro6p_0M78El6xpS8Z0wnA)
- Training dataset 2, including NJUD(1485) and NLPR(700), DUT-RGBD(800), [fetch code is 2985](https://pan.baidu.com/s/1A3U3KsaO4RzCeQArEiy1kA)
- Besides, we also provide a set of training dataset with data augmentation, which contains 2985*11=32835 samples, [fetch code is taug](https://pan.baidu.com/s/1GyT0zeFrdMJROhc4iA95zg)

****

### Evaluation tools

****

### Pre-trained tools
将网络生成的sal maps放到evaluation_tool文件夹下，运行calculate metrics即可计算评价指标

****
