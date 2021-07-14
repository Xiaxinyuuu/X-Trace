
# X-Trace
> **“"X-Trace" pedestrian tracking system combines pedestrian detection and pedestrian tracking technology, and the overall performance of detection and Re-ID is excellent. The software has a complete architecture, beautiful interface, comprehensive functions, and friendly interaction. It can be widely used in intelligent video surveillance and intelligent security. And other fields**。



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.



### Installation

* Clone this repo, and we'll call the directory that you cloned as ${X-Trace}
* Install dependencies. We use python 3.7 and CUDA10.2 

```
conda create -n X-Trace
conda activate X-Trace
cd ${X-Trace}
pip install -r requirements.txt
```

### 

### Start
1.You can start the software quickly by running main.py

```
python main_pyqt.py
```

2.You can start detecting videos or images by running demo.py
```
python demo.py --video_path {your video_path} --threshold {threshold}
```



### Authors
**XiaXinyu** and **ZhangYuxuan**

### License

This project is licensed under the Apache Licence 2.0


### Acknowledgments
A large part of the code is borrowed from [ZQPei/deep_sort_pytorch](https://github.com/ZQPei/deep_sort_pytorch) and [寂寞你快进去/行人重识别：基于度量学习的行人重识别算法](https://aistudio.baidu.com/aistudio/projectdetail/1199726) . Thanks for their wonderful works.
