import cv2

from PyQt5 import QtWidgets, QtCore, QtGui
from detector import Detector

from total import Ui_TOTAL

global Det, camflag

class CamModule(QtWidgets.QMainWindow, Ui_TOTAL):
    def __init__(self):
        global Det, camflag
        super(CamModule, self).__init__()
        self.setupUi(self)
        camflag = 0
        # 检测器初始化
        Det = Detector(track=True)
        try:
            # 线程实例化
            self.cam_thread = Cam_Thread()
            self.cam_thread.signal.connect(self.Cam_connect)
            self.cam_thread.finish_sig.connect(self.cam_off)
            print("cam succeeded")
        except:
            print("cam error")

    def Camera(self):
        global _thros
        self.camera.hide()
        self.camera_off.show()
        self.represent_cam.show()
        _thros = self.Slider_3.value() * 0.01
        self.threshold_cam.setText(f'%.2f' % _thros)
        self.cam_thread.start()

    def Cam_connect(self):
        global cam_frame, pedestrian_total, confidence_coefficient
        try:
            # 图片居中
            self.represent_cam.setAlignment(QtCore.Qt.AlignCenter)
            # 图片适应窗口大小
            self.represent_cam.setScaledContents(True)
            # 通道转化
            RGBImg = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
            # 将图片转化成Qt可读格式
            cam_frame = QtGui.QImage(RGBImg, RGBImg.shape[1], RGBImg.shape[0], RGBImg.shape[1] * 3,
                                     QtGui.QImage.Format_RGB888)
            self.represent_cam.setPixmap(QtGui.QPixmap.fromImage(cam_frame))
            self.count_cam.setText("{}人".format(pedestrian_total))
            self.confidence_coefficient_cam.setText("{}".format(confidence_coefficient))
        except:
            pass

    def make_camoff(self):
        global camflag
        camflag = 1

    def cam_off(self):
        global camflag
        self.camera.show()
        self.camera_off.hide()
        self.represent_cam.clear()
        self.threshold_cam.setText("阈值调控")
        self.count_cam.setText("人数")
        self.confidence_coefficient_cam.setText("置信度")
        self.camera_off.hide()
        self.camera.show()
        camflag = 0

class Cam_Thread(QtCore.QThread, Ui_TOTAL):
    signal = QtCore.pyqtSignal()
    finish_sig = QtCore.pyqtSignal()
    def __init__(self):
        super(Cam_Thread, self).__init__()

    def run(self):
        global cam_frame, pedestrian_total, confidence_coefficient, _thros, Det, camflag
        # 摄像头协程初始化
        Cam = Det.rlt_detect(threshold=_thros)
        while True:
            try:
                cam_frame, pedestrian_total, confidence_coefficient = Cam.send(None)
                self.signal.emit()
                if camflag == 1:
                    self.finish_sig.emit()
                    break
            except:
                pass