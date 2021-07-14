from detector import Detector
import time
Det = Detector()


#1.检测图片
a = time.time()
# Det.img_detect(['E:\python\Competition\PYQT\images\\test\MOT20-04\img1.000001.jpg'],threshold = 0.5)#输入图片路径,方法返回一张图片
print(time.time()-a)
# 2.检测视频
# Det.video_detect('E:\Towards-Realtime-MOT-master_new\\MOT_new00.mp4', threshold=0.2,) #第一个参数：视频路径，默认保存为./result.avi即当前路径下result.avi文件
# #3.打开摄像头实时检测
# Det.rlt_detect(threshold=0.1)
# 跨镜
# Det.ReID(['E:\python\Competition\PYQT\\videos\\demo1.avi', "E:\python\Competition\PYQT\\videos\\demo0.avi"],img='E:\python\Competition\PYQT\images\\01target.jpg')
import cv2

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter('0.avi', fourcc, 30, (1035, 679), True)


