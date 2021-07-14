import os, cv2, shutil

from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets, QtCore, QtGui
from detector import Detector

from total import Ui_TOTAL

global pedestrian_total, confidence_coefficient, threshold, result, ls2, Det, img_fileLists, img_info


class PicModule(QtWidgets.QMainWindow, Ui_TOTAL):
    def __init__(self):
        super(PicModule, self).__init__()
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        try:
            # 线程实例化
            self.img_thread = Img_Thread()
            self.img_thread.signal.connect(self.Img_Connect)
            print("pic succeeded")
        except:
            print("pic error")
        # 判断result文件夹是否存在
        if not os.path.exists("temp_imgs"):
            os.mkdir("temp_imgs")

    # 图片选择
    def ChooseImages(self):
        global pedestrian_total, img_fileLists
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       "请选择图片",
                                                       "E:\python\Competition\PYQT\pics",  # 起始路径
                                                       "Image Files(*.jpg *.jpeg *.png *.bmp *.svg *.ico)")  # 设置文件扩展名过滤

        if len(files) == 0:
            return
        else:
            img_fileLists = files
            self.imglist_add1()
            self.reselect_img.show()
            self.Slider.show()
            self.label.show()
            self.label_6.show()
            self.picture.hide()
            self.pic.hide()
            self.submit_img.show()
            _thros = self.Slider.value() * 0.01
            self.threshold_img.setText(f"%.2f" % _thros)
            self.count_img.setText("行人数量")
            self.confidence_coefficient_img.setText("置信度")

    def Submit_img(self):
        global threshold, Det
        self.img_list.clear()
        self.Slider.hide()
        self.label.hide()
        self.label_6.hide()
        self.represent_img.clear()
        self.waiting.show()
        self.submit_img.hide()
        self.reselect_img.hide()
        # 获取滑动条的值, 并传给模型使用
        threshold = self.Slider.value() * 0.01
        # 检测器初始化
        Det = Detector(img_arr=img_fileLists)
        self.img_thread.start()

    def Reselect_img(self):
        global img_info
        img_info = []
        self.represent_img.clear()
        self.pic.show()
        self.allchecked.hide()
        self.allunchecked.hide()
        self.save.hide()
        self.reselect_img.hide()
        self.reselect_img.setGeometry(850, 720, 161, 41)
        self.submit_img.hide()
        self.picture.show()
        self.Slider.hide()
        self.label.hide()
        self.label_6.hide()
        self.count_img.setText("行人数量")
        self.confidence_coefficient_img.setText("置信度")
        self.threshold_img.setText("阈值控制")
        self.img_list.clear()
        self.ChooseImages()

    def imglist_add1(self):
        global img_fileLists
        for file in img_fileLists:
            item = QtWidgets.QListWidgetItem(file)
            self.img_list.addItem(item)
        self.img_list.setCurrentItem(self.img_list.item(0))
        self.imglist_clicked(self.img_list.item(0))

    def imglist_add2(self):
        for _ in os.listdir("./temp_imgs"):
            _ = "./temp_imgs/" + _
            item = QtWidgets.QListWidgetItem(_)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.img_list.addItem(item)
        self.img_list.setCurrentItem(self.img_list.item(0))
        self.imglist_clicked(self.img_list.item(0))

    def imglist_clicked(self, item):
        global ls2, img_info
        self.represent_img.setAlignment(QtCore.Qt.AlignCenter)    # 图片居中
        self.represent_img.setScaledContents(True)    #图片适应窗口
        self.represent_img.setPixmap(QtGui.QPixmap(item.text()))
        # 将选中的item添加到列表中
        ls1 = []  # 判断是否为全选列表
        ls2 = []  # 添加元素到此列表中
        for i in range(self.img_list.count()):
            if self.img_list.item(i).checkState():
                ls1.append(2)
                ls2.append(self.img_list.item(i).text())

            elif not self.img_list.item(i).checkState():
                ls1.append(0)
                try:
                    ls2.pop(self.img_list.item(i).text())
                except:
                    pass
        # 判断是否全选, 并对按钮做出改变
        ls1.sort()
        length = len(ls1)
        if ls1[0] != ls1[length - 1]:
            self.allchecked.show()
            self.allunchecked.hide()
        elif ls1[0] == ls1[length - 1] and ls1[0] == 2:
            self.allunchecked.show()
            self.allchecked.hide()
        # 单个图片显示人数和置信度
        count = 0
        try:
            for key, value in img_info[self.img_list.currentRow()].items():
                if count:
                    self.confidence_coefficient_img.setText(f"%.4f" % value)
                if not count:
                    self.count_img.setText(f"%d" % value)

                count += 1
        except (NameError, IndexError):
            self.count_img.setText("行人数量")
            self.confidence_coefficient_img.setText("置信度")

    def all_checked(self):
        for i in range(self.img_list.count()):
            items = self.img_list.item(i)
            if items.checkState():
                continue
            else:
                items.setCheckState(QtCore.Qt.Checked)
            self.imglist_clicked(items)
        self.allunchecked.show()
        self.allchecked.hide()

    def all_unchecked(self):
        for i in range(self.img_list.count()):
            items = self.img_list.item(i)
            items.setCheckState(QtCore.Qt.Unchecked)
            self.imglist_clicked(items)
        self.allchecked.show()
        self.allunchecked.hide()

    def Save_Img(self):
        global ls2
        # 若复选图片列表为空, 则显示此信息
        if not ls2:
            QtWidgets.QMessageBox.information(self,
                                          "信息", "请至少选择一张图片",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            return
        # 文件保存
        QtWidgets.QMessageBox.warning(self,
                                      "警告", "保存的文件名不可以有中文, 不然可能会保存失败",
                                      QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "图片保存",  # 窗口名
                                                                "E:\python\Competition\PYQT\save",  # 对话框默认显示路径
                                                                "")
        if fileName_choose:
            cnt = 1
            for i in ls2:
                i = cv2.imread(i)
                cv2.imwrite("{1}{0}.jpg".format(cnt, fileName_choose), i)
                cnt += 1
            QtWidgets.QMessageBox.information(self, "提示", "文件保存成功!",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            return

    def Img_Connect(self):
        self.save.show()
        self.reselect_img.show()
        self.submit_img.hide()
        self.save.show()
        self.allchecked.show()
        self.reselect_img.setGeometry(545, 720, 161, 41)
        self.waiting.hide()
        self.imglist_add2()


# 多线程
class Img_Thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(Img_Thread, self).__init__()

    def run(self):
        global result, Det, threshold, img_fileLists, img_info
        # 清空result文件夹
        shutil.rmtree("temp_imgs")
        os.mkdir("temp_imgs")
        try:
            img_info = Det.img_detect(threshold=threshold)
        except NameError:
            img_info = Det.img_detect(threshold=0.5)
        self.signal.emit(str())