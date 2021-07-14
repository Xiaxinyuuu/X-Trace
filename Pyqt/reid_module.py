import cv2

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from detector import Detector
from total import *

global Vdo_fileNames, Det_reID, vdos_list, judge, img_, hit_num, pics_list, infos, Det, pics_num


class ReIDModule(QMainWindow, Ui_TOTAL):
    def __init__(self):
        super(ReIDModule, self).__init__()
        self.setupUi(self)
        global Det_reID, judge, Det
        # 模型初始化
        Det = Detector()
        print("reID succeeded")
        # 线程实例化
        self.reid_thread = ReID_Thread()
        self.reid_thread.reid_signal.connect(self.reID_connect)
        self.reid_thread.reid_finish.connect(self.reID_finish)
        self.reid_thread.reid_represent.connect(self.reID_represent)
        judge = 0

    # 选择视频
    def ChooseVideos(self):
        global Vdo_fileNames, Det_reID, vdos_list, judge
        file_vdos, filetype = QFileDialog.getOpenFileNames(self,
                                                       "请选择图片",
                                                       "E:\python\Competition\PYQT\\videos",  # 起始路径
                                                       "Video Files(*.mp4 *.avi *.rmvb *.wmv *.flv *.mpeg *.ogg)")  # 设置文件扩展名过滤

        if len(file_vdos) == 0:
            return
        else:
            Vdo_fileNames = file_vdos
            self.videos.hide()
            self.reID_vdo.hide()
            vdos_list = Det.get_img(Vdo_fileNames)
            for _ in vdos_list:
                RGBImg = cv2.cvtColor(_, cv2.COLOR_BGR2RGB)
                # 将图片转化成Qt可读格式
                first_frame = QImage(RGBImg, RGBImg.shape[1], RGBImg.shape[0], RGBImg.shape[1] * 3,
                                   QImage.Format_RGB888)
                # 创建listwidget项目
                item = QListWidgetItem(QIcon(QPixmap.fromImage(first_frame)), "")
                # 设置列表图标大小
                self.vdolist.setIconSize(QSize(590, 590))
                # 设置为显示图片模式
                self.vdolist.setViewMode(QListView.IconMode)
                # 图片适应
                self.vdolist.setResizeMode(QListWidget.Adjust)
                # 图片禁止拖动
                self.vdolist.setMovement(QListWidget.Static)
                # 添加
                self.vdolist.addItem(item)
            judge += 1
            if judge == 2:
                self.reID_revdo.setGeometry(780, 750, 161, 41)
                self.reID_revdo.show()
                self.reID_submit.show()
                self.label_20.show()
                self.label_21.show()
                self.hitnum.show()
                judge = 0
            else:
                self.reID_revdo.setGeometry(530, 750, 161, 41)
                self.reID_revdo.show()

    # 重选视频
    def re_vdo(self):
        global judge
        self.videos.show()
        self.reID_vdo.show()
        self.reID_revdo.hide()
        self.vdolist.clear()
        self.reID_submit.hide()
        self.label_20.hide()
        self.label_21.hide()
        judge = 1

    # 选择目标图片
    def ChooseImage(self):
        global img_, judge
        file_img, filetype = QFileDialog.getOpenFileName(self,
                                                        "请选择目标图片",
                                                        "E:\python\Competition\PYQT\images\\target",  # 起始路径
                                                        "Image Files(*.jpg *.jpeg *.png *.bmp *.svg *.ico)") # 设置文件扩展名过滤,用双分号间隔

        if file_img == "":
            return
        else:
            img_ = file_img
            self.targetpic.setPixmap(QPixmap(img_))
            self.tarperson.hide()
            self.tarperson_btn.hide()
            # 图片居中
            self.targetpic.setAlignment(QtCore.Qt.AlignCenter)
            # 自适应窗口大小
            self.targetpic.setScaledContents(True)
            judge += 1
            if judge == 2:
                self.reID_revdo.setGeometry(780, 750, 161, 41)
                self.reID_reperson.show()
                self.reID_submit.show()
                self.label_20.show()
                self.label_21.show()
                self.hitnum.show()
                judge = 0
            else:
                self.reID_revdo.setGeometry(530, 750, 161, 41)
                self.reID_reperson.show()

    # 重选目标图片
    def re_tarperson(self):
        global judge
        self.tarperson.show()
        self.tarperson_btn.show()
        self.reID_reperson.hide()
        self.targetpic.clear()
        self.reID_submit.hide()
        self.label_20.hide()
        self.label_21.hide()
        judge = 1

    # 查询按钮
    def reID_search(self):
        global hit_num
        hit_num = int(self.hitnum.text())-1
        self.reID_submit.hide()
        self.reID_revdo.hide()
        self.reID_reperson.hide()
        self.reID_res.setGeometry(400, 110, 451, 50)
        self.reID_progressBar.show()
        self.label_19.show()
        self.pics_num.show()
        self.reID_res.setText("正在从视频里查找目标中...")
        self.hitnum.setEnabled(False)
        self.hitnum.setCursor(Qt.ArrowCursor)
        self.reid_thread.start()

    def reID_connect(self):
        global Det_reID, Vdo_fileNames, img_, hit_num, pics_list, infos, pics_num
        self.pics_num.setText(str(pics_num))

    def reID_finish(self):
        self.reID_res.hide()
        self.sort_cmp.show()

    def reID_represent(self):
        self.sort_cmp.hide()
        self.reID_progressBar.hide()
        self.label_19.hide()
        self.pics_num.hide()
        for i, j in zip(pics_list, infos):
            RGBImg = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
            # 将图片转化成Qt可读格式
            first_frame = QImage(RGBImg, RGBImg.shape[1], RGBImg.shape[0], RGBImg.shape[1] * 3,
                                 QImage.Format_RGB888)
            # 创建listwidget项目
            item = QListWidgetItem(QIcon(QPixmap.fromImage(first_frame)), f"视频%d的第%.1f秒处" % (j[0]+1, j[1]))
            # 设置列表图标大小
            self.reslist.setIconSize(QSize(590, 590))
            # 设置为显示图片模式
            self.reslist.setViewMode(QListView.IconMode)
            # 图片适应
            self.reslist.setResizeMode(QListWidget.Adjust)
            # 图片禁止拖动
            self.reslist.setMovement(QListWidget.Static)
            # 添加
            self.reslist.addItem(item)
        self.reIDbtn.show()

    # 全部重选
    def reID_re(self):
        self.videos.show()
        self.reID_vdo.show()
        self.tarperson.show()
        self.tarperson_btn.show()
        self.targetpic.clear()
        self.vdolist.clear()
        self.reslist.clear()
        self.reIDbtn.hide()

#  跨镜线程
class ReID_Thread(QThread):
    reid_signal = pyqtSignal()
    reid_finish = pyqtSignal()
    reid_represent = pyqtSignal()
    def __init__(self):
        super(ReID_Thread, self).__init__()

    def run(self):
        global Det_reID, Vdo_fileNames, img_, hit_num, pics_list, infos, Det, pics_num
        Det_reID = Det.ReID(videos=Vdo_fileNames, img=img_, hit_num=hit_num)
        while True:
            try:
                pics_list, infos, pics_num = Det_reID.send(None)
                self.reid_signal.emit()
            except StopIteration:
                try:
                    self.reid_finish.emit()
                    pics_list, infos, pics_num = Det_reID.send(None)
                except StopIteration:
                    self.reid_represent.emit()
                    break
