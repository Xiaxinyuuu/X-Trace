import sys
from PyQt5.QtWidgets import QDesktopWidget

from pic_module import *
from vdo_module import *
from cam_module import *
from reid_module import *

global Vdo_fileName, pedestrian_total, confidence_coefficient, threshold, result, img, cam_frame, Det_vdo, ls2, vdo_frame

class Total(VdoModule, PicModule, CamModule, ReIDModule, ChartsWindow):
    def __init__(self):
        super(Total, self).__init__()
        # 禁止使用最大化按钮
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |
                            QtCore.Qt.WindowCloseButtonHint)
        # 禁止窗口大小拖动
        self.setFixedSize(self.width(), self.height())
        # 文件保存
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        # 窗口居中
        self.center()
        # 实体隐藏
        # 图片
        self.save.hide()
        self.Slider.hide()
        self.submit_img.hide()
        self.reselect_img.hide()
        self.label.hide()
        self.label_6.hide()
        self.allchecked.hide()
        self.allunchecked.hide()
        self.waiting.hide()
        # 视频
        self.reselect_vdo.hide()
        self.submit_vdo.hide()
        self.Slider_2.hide()
        self.label_3.hide()
        self.label_7.hide()
        self.label_16.hide()
        self.person_counting.hide()
        self.ROI_btn.hide()
        self.progressBar.hide()
        self.count_vdo_ROI.hide()
        self.count_vdo_total.hide()
        self.viewcount_vdo_ROI.hide()
        self.viewcount_vdo_total.hide()
        self.label_12.hide()
        # 摄像头
        self.camera_off.hide()
        # 跨镜
        self.reID_submit.hide()
        self.reID_progressBar.hide()
        self.reID_revdo.hide()
        self.reID_reperson.hide()
        self.label_19.hide()
        self.label_20.hide()
        self.label_21.hide()
        self.pics_num.hide()
        self.sort_cmp.hide()
        self.hitnum.hide()
        self.reIDbtn.hide()
        self.reID_res.setGeometry(477, 160, 266, 50)

        # 滑动条显示小数
        self.Slider.valueChanged['int'].connect(self.setfloat1)
        self.Slider_2.valueChanged['int'].connect(self.setfloat2)
        self.Slider_3.valueChanged['int'].connect(self.setfloat3)

    # 窗口居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 滑动条显示小数
    def setfloat1(self, value):
        float = value * 0.01
        self.threshold_img.setText(f"%.2f" % float)

    def setfloat2(self, value):
        global threshold
        float = value * 0.01
        self.threshold_vdo.setText(f"%.2f" % float)

    def setfloat3(self, value):
        global threshold
        float = value * 0.01
        self.threshold_cam.setText(f"%.2f" % float)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        close_info = QMessageBox()
        event = QMessageBox.information(close_info, "关闭窗口", "确认退出窗口？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if event == QMessageBox.Yes:
            a0.accept()
            os._exit(5)
        else:
            a0.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    total = Total()
    total.show()

    total.save.clicked.connect(total.Save_Img)
    total.picture.clicked.connect(total.ChooseImages)
    total.submit_img.clicked.connect(total.Submit_img)
    total.reselect_img.clicked.connect(total.Reselect_img)
    total.allchecked.clicked.connect(total.all_checked)
    total.allunchecked.clicked.connect(total.all_unchecked)
    total.img_list.itemClicked.connect(total.imglist_clicked)
    # 视频
    total.video.clicked.connect(total.ChooseVideo)
    total.submit_vdo.clicked.connect(total.Submit_vdo)
    total.ROI_btn.clicked.connect(total.ROI_submit)
    total.reselect_vdo.clicked.connect(total.make_vdooff)
    total.person_counting.clicked.connect(lambda: total.charts_win.show())
    total.history.clicked.connect(total.histories_win.winshow)
    total.idBox.textHighlighted.connect(total.thread_lock)
    total.idBox.activated.connect(total.thread_unlock)
    # 摄像头
    total.camera.clicked.connect(total.Camera)
    total.camera_off.clicked.connect(total.make_camoff)
    # 跨镜
    total.reID_vdo.clicked.connect(total.ChooseVideos)
    total.reID_revdo.clicked.connect(total.re_vdo)
    total.tarperson_btn.clicked.connect(total.ChooseImage)
    total.reID_reperson.clicked.connect(total.re_tarperson)
    total.reID_submit.clicked.connect(total.reID_search)
    total.reIDbtn.clicked.connect(total.reID_re)

    sys.exit(app.exec_())
