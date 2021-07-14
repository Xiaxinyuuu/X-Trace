import os, cv2, win32gui

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtMultimedia import *

from detector import Detector
from total import *
from charts import *
from charts_represent import *
from history_win import *
from sqlite import *
from vdoplay import *

global Vdo_fileName, pedestrian_total, ROI_pedestrian_total, confidence_coefficient, threshold, value, vdo_flag
global result, Det_vdo, vdo_frame, Det, ids, browser, flag, lock_flag, frames_num, current, person_id, vdo_path


class VdoModule(QtWidgets.QMainWindow, Ui_TOTAL):
    def __init__(self):
        global Det, lock_flag, ls1, ls2, vdo_flag
        super(VdoModule, self).__init__()
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        # 线程睡眠标志
        lock_flag = 0
        # 停止线程标志
        vdo_flag = 0
        # 线程实例化
        self.vdo_thread = Vdo_Thread()
        self.vdo_thread.signal.connect(self.Vdo_Connect)
        self.vdo_thread.finished.connect(self.finished)
        self.vdo_thread.finish_vdo.connect(self.Reselect_vdo)
        # 实例化
        self.charts_win = ChartsWindow()
        self.histories_win = HistoryWindow()
        # 设置qcombobox最大显示数据个数
        self.idBox.setMaxVisibleItems(10)
        print("vdo succeeded")
        # 判断文件夹是否存在
        if not os.path.exists("temp_vdo"):
            os.mkdir("temp_vdo")


    # 选择视频
    def ChooseVideo(self):
        global Vdo_fileName, Det_vdo, pedestrian_total, confidence_coefficient, vdo_frame, Det, ids, frames_num
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "选取视频",
                                                                "E:\python\Competition\PYQT\\videos",  # 起始路径
                                                                "Video Files(*.mp4 *.avi *.rmvb *.wmv *.flv *.mpeg *.ogg)")  # 设置文件扩展名过滤
        if fileName_choose == "":
            return
        else:
            Vdo_fileName = fileName_choose
            self.video.hide()
            self.submit_vdo.show()
            self.reselect_vdo.show()
            self.Slider_2.show()
            self.label_3.show()
            self.label_7.show()
            # 视频第一帧
            try:
                _thros = self.Slider_2.value()*0.01
                self.threshold_vdo.setText(f"%.2f" % _thros)
                Det = Detector(video_path="{}".format(Vdo_fileName), track=True)  # 检测器初始化
                vdo_frame = Det.get_img([Vdo_fileName])
                for _ in vdo_frame:
                    vdo_frame = _
                RGBImg = cv2.cvtColor(vdo_frame, cv2.COLOR_BGR2RGB)
                # 将图片转化成Qt可读格式
                vdo_frame = QImage(RGBImg, RGBImg.shape[1], RGBImg.shape[0], RGBImg.shape[1] * 3,
                                         QImage.Format_RGB888)

                # 图片居中
                self.represent_vdo.setAlignment(QtCore.Qt.AlignCenter)
                # 自适应窗口大小
                self.represent_vdo.setScaledContents(True)
                self.represent_vdo.setPixmap(QPixmap.fromImage(vdo_frame))
                # 获取视频总帧数
                cap = cv2.VideoCapture("{}".format(Vdo_fileName))
                frames_num = cap.get(7)
                self.history.hide()
                self.represent_vdo.show()
                self.ROI_btn.show()
                self.reselect_vdo.setGeometry(850, 720, 161, 41)
            except StopIteration:
                return

    # 开始识别按钮
    def Submit_vdo(self):
        global threshold, flag, Det_vdo, Det, vdo_flag
        vdo_flag = 0
        self.submit_vdo.hide()
        self.vdo.hide()
        self.Slider_2.hide()
        self.label_3.hide()
        self.label_7.hide()
        self.ROI_btn.hide()
        self.person_counting.show()
        self.label_16.show()
        self.reselect_vdo.setGeometry(950, 720, 161, 41)
        self.progressBar.show()
        threshold = self.Slider_2.value() * 0.01
        flag = 0
        Det_vdo = Det.video_detect(threshold=threshold)
        self.vdo_thread.start()

    # ROI识别按钮
    def ROI_submit(self):
        global threshold, flag, Det_vdo, vdo_flag
        vdo_flag = 0
        self.submit_vdo.hide()
        self.vdo.hide()
        self.Slider_2.hide()
        self.label_3.hide()
        self.label_7.hide()
        self.ROI_btn.hide()
        self.person_counting.show()
        self.count_vdo.hide()
        self.count_vdo_ROI.show()
        self.label_16.show()
        self.count_vdo_total.show()
        self.viewcount_vdo_ROI.show()
        self.viewcount_vdo_total.show()
        self.label_12.show()
        self.progressBar.show()
        self.reselect_vdo.setGeometry(950, 720, 161, 41)
        threshold = self.Slider_2.value() * 0.01
        flag = 1
        QtWidgets.QMessageBox.information(self, "提示信息", "在弹出的对话框中, 顺次在图像上点击四个点, 按'Q'键结束",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        Det = Detector(video_path="{}".format(Vdo_fileName), track=True, ROI=True)  # 检测器初始化
        Det_vdo = Det.video_detect(threshold=threshold, video_cnt=1)
        self.vdo_thread.start()

    # 重选视频按钮
    def Reselect_vdo(self):
        global flag
        flag = 0
        self.vdo.show()
        self.represent_vdo.clear()
        self.reselect_vdo.hide()
        self.video.show()
        self.submit_vdo.hide()
        self.Slider_2.hide()
        self.label_3.hide()
        self.label_7.hide()
        self.label_16.hide()
        self.person_counting.hide()
        self.count_vdo_ROI.hide()
        self.count_vdo_total.hide()
        self.viewcount_vdo_ROI.hide()
        self.viewcount_vdo_total.hide()
        self.ROI_btn.hide()
        self.history.show()
        self.label_12.hide()
        self.count_vdo.show()
        self.count_vdo.setText("行人数量")
        self.confidence_coefficient_vdo.setText("置信度")
        self.threshold_vdo.setText("阈值调控")
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.xmin.setText("0")
        self.ymin.setText("0")
        self.xmax.setText("0")
        self.ymax.setText("0")
        self.idBox.clear()
        self.ChooseVideo()

    # 线程锁定
    def thread_lock(self):
        global lock_flag
        lock_flag = 1

    # 线程解锁
    def thread_unlock(self):
        global lock_flag, value, Det_vdo, flag
        value = self.idBox.currentText()
        if flag:
            if value == "所有行人":
                Det_vdo = Det.video_detect(threshold=threshold, ID=None, video_cnt=0)
            else:
                Det_vdo = Det.video_detect(threshold=threshold, ID=int(value), video_cnt=0)
            lock_flag = 0
        else:
            if value == "所有行人":
                Det_vdo = Det.video_detect(threshold=threshold, ID=None)
            else:
                Det_vdo = Det.video_detect(threshold=threshold, ID=int(value))
            lock_flag = 0

    # 帧线程信号接收
    def Vdo_Connect(self):
        global pedestrian_total, ROI_pedestrian_total, confidence_coefficient, vdo_frame
        global flag, current, frames_num, value

        try:
            # 进度条
            self.progressBar.setValue(int((current / frames_num + 0.02) * 100))
            # 颜色通道转化
            RGBImg = cv2.cvtColor(vdo_frame, cv2.COLOR_BGR2RGB)
            # 将图片转化成Qt可读格式
            vdo_frame = QImage(RGBImg, RGBImg.shape[1], RGBImg.shape[0], RGBImg.shape[1] * 3,
                                     QImage.Format_RGB888)
            # 图片居中
            self.represent_vdo.setAlignment(QtCore.Qt.AlignCenter)
            # 自适应窗口大小
            self.represent_vdo.setScaledContents(True)
            # 帧显示
            self.represent_vdo.setPixmap(QPixmap.fromImage(vdo_frame))
            if flag:
                # 行人总数
                self.count_vdo_total.setText("{}人".format(pedestrian_total))
                # ROI行人数量
                self.count_vdo_ROI.setText("{}人".format(ROI_pedestrian_total))
            else:
                # 行人数量
                self.count_vdo.setText("{}人".format(pedestrian_total))
            # 置信度
            self.confidence_coefficient_vdo.setText("{}".format(confidence_coefficient))
            #行人id
            self.id_box()
            # 行人坐标显示
            try:
                self.xmin.setText(str(int(ids[value][0])))
                self.ymin.setText(str(int(ids[value][1])))
                self.xmax.setText(str(int(ids[value][2])))
                self.ymax.setText(str(int(ids[value][3])))
            except NameError:
                pass
        except:
            pass

    # 行人id算法
    def id_box(self):
        global ids

        ls1 = []
        ls2 = []
        ls3 = []
        ls4 = []

        for _ in range(self.idBox.count()):
            ls1.append(self.idBox.itemText(_))
        for _ in ids.keys():
            ls2.append(_)

        for i, _ in enumerate(ls1):
            if _ not in ls2:
                ls3.append(i)

        for i, _ in enumerate(ls2):
            if _ not in ls1:
                ls4.append(_)

        lens = len(ls3) - len(ls4)
        if lens < 0:
            for _ in range(len(ls3)):
                self.idBox.removeItem(ls3[_])
                self.idBox.addItem(str(ls4[_]))
            for i in range(len(ls3), len(ls4)):
                self.idBox.addItem(str(ls4[i]))

        if lens == 0:
            for _ in range(len(ls3)):
                self.idBox.removeItem(ls3[_])
                self.idBox.addItem(str(ls4[_]))

        if lens > 0:
            for _ in range(len(ls4)):
                self.idBox.removeItem(ls3[_])
                self.idBox.addItem(str(ls4[_]))
            for i in range(len(ls3), len(ls4), -1):
                self.idBox.removeItem(ls3[i - 1])

    # 结束信息
    def finished(self):
        info = QMessageBox()
        QMessageBox.information(info, "信息", "视频识别完成", QMessageBox.Ok, QMessageBox.Ok)

    # 使线程停止
    def make_vdooff(self):
        global vdo_flag
        vdo_flag = 1
        time.sleep(0.1)
        self.Reselect_vdo()

# 帧播放线程
class Vdo_Thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    finished = pyqtSignal(str)
    finish_vdo = pyqtSignal()
    def __init__(self):
        super(Vdo_Thread, self).__init__()
        # 线程实例化
        self.creatchart = ChartsThread()
        self.creatchart.chart_signal.connect(ChartsWindow.chartsignal_connect)

    def run(self):
        global vdo_frame, pedestrian_total, ROI_pedestrian_total, confidence_coefficient
        global Det, threshold, ids, Det_vdo, flag, lock_flag, current, value, vdo_flag
        self.creatchart.start()
        # 实例化
        if flag:
            while True:
                try:
                    vdo_frame, pedestrian_total, ROI_pedestrian_total, confidence_coefficient, ids, current = Det_vdo.send(None)
                    # 线程信号发射
                    self.signal.emit(str())
                    self.msleep(100)
                    # 线程锁
                    while True:
                        if lock_flag == 1:
                            self.msleep(10)
                        elif lock_flag == 0:
                            break
                    # 线程停止
                    if vdo_flag == 1:
                        break
                except StopIteration:
                    self.finished.emit(str())
                    break
        else:
            while True:
                try:
                    vdo_frame, pedestrian_total, confidence_coefficient, ids, current = Det_vdo.send(None)
                    # 线程信号发射
                    self.signal.emit(str())
                    self.msleep(100)
                    # 线程锁
                    while True:
                        if lock_flag == 1:
                            self.msleep(10)
                        elif lock_flag == 0:
                            break
                    # 线程停止
                    if vdo_flag == 1:
                        break
                except StopIteration:
                    self.finished.emit(str())
                    break
# 图表窗口
class ChartsWindow(QtWidgets.QMainWindow, Ui_Charts_Represent):
    def __init__(self):
        global browser
        super(ChartsWindow, self).__init__()
        self.setupUi(self)
        # 禁止使用最大化按钮
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        # 禁止窗口大小拖动
        self.setFixedSize(self.width(), self.height())
        # 创建WebEngine实例
        browser = QWebEngineView()
        self.setCentralWidget(browser)

    # 创建图表线程信号接收
    def chartsignal_connect(self):
        browser.load(QtCore.QUrl('file:///person_counting.html'))

# 数据传递并绘制线程
class ChartsThread(QtCore.QThread):
    chart_signal = QtCore.pyqtSignal(QWebEngineView)
    def __init__(self):
        super(ChartsThread, self).__init__()

    def run(self):
        global pedestrian_total, count
        times = 1
        count = 1
        # 图表实例化
        area = Area()
        area.send(None)
        while True:
            try:
                dic = {"times": times, "nums": pedestrian_total}
                area.send(dic)
                self.msleep(100)
                times += 1
                # 线程停止
                if win32gui.FindWindow(0, "选取视频") or win32gui.FindWindow(0, "信息"):
                    break
                # 图表窗口显示
                if count > 15:
                    self.chart_signal.emit(QWebEngineView())
                    self.msleep(100)
                    count = 1
                count += 1
                # 线程锁
                while True:
                    if lock_flag:
                        self.msleep(10)
                    else:
                        break
            except NameError:
                pass

# 视频播放器
class VideoPlayer(QDialog, Ui_VideoPlayer):
    def __init__(self):
        super(VideoPlayer, self).__init__()
        self.setupUi(self)

    def play_run(self):
        global vdo_path
        self.show()
        self.play.hide()
        # 创建视频播放器
        self.player = QMediaPlayer(self)
        # 显示视频组件
        self.player.setVideoOutput(self.video)
        # 视频源
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(vdo_path)))
        # 按钮
        self.play.clicked.connect(self.playbtn)
        self.pause.clicked.connect(self.pausebtn)
        # 进度条
        self.player.durationChanged.connect(self.getDuration)
        self.player.positionChanged.connect(self.getPosition)
        self.progress.sliderMoved.connect(self.updatePosition)
        # 播放
        self.player.play()

    # 播放视频
    def playbtn(self):
        self.pause.show()
        self.play.hide()
        self.player.play()

    # 暂停视频
    def pausebtn(self):
        self.pause.hide()
        self.play.show()
        self.player.pause()

    # 视频总时长获取
    def getDuration(self, d):
        """d是获取到的视频总时长（ms）"""
        minutes = int(d/60000)
        seconds = int(d/1000)
        if int(seconds / 10) == 0 and int(minutes / 10) == 0:
            self.alltime.setText('0{}:0{}'.format(minutes, seconds))
        elif int(seconds / 10) == 0 and int(minutes / 10) != 0:
            self.alltime.setText('{}:0{}'.format(minutes, seconds))
        elif int(seconds / 10) != 0 and int(minutes / 10) == 0:
            self.alltime.setText('0{}:{}'.format(minutes, seconds))
        else:
            self.alltime.setText('{}:{}'.format(minutes, seconds))
        self.progress.setRange(0, d)
        self.progress.setEnabled(True)
        self.displayTime(d)

    # 视频实时位置获取
    def getPosition(self, p):
        self.progress.setValue(p)
        self.displayTime(self.progress.maximum() - p)

    # 显示剩余时间
    def displayTime(self, ms):
        minutes = int(ms / 60000)
        seconds = int(ms/ 1000)
        if int(seconds / 10) == 0 and int(minutes / 10) == 0:
            self.subtime.setText('0{}:0{}'.format(minutes, seconds))
        elif int(seconds / 10) == 0 and int(minutes / 10) != 0:
            self.subtime.setText('{}:0{}'.format(minutes, seconds))
        elif int(seconds / 10) != 0 and int(minutes / 10) == 0:
            self.subtime.setText('0{}:{}'.format(minutes, seconds))
        else:
            self.subtime.setText('{}:{}'.format(minutes, seconds))

    # 用进度条更新视频位置
    def updatePosition(self, v):
        self.player.setPosition(v)
        self.displayTime(self.progress.maximum() - v)

    def closeEvent(self, a0: QCloseEvent):
        # time.sleep(0.01)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("./temp_vdo/0.avi")))
        self.player.play()

# 历史记录窗口
class HistoryWindow(QDialog, Ui_History):
    def __init__(self):
        super(HistoryWindow, self).__init__()
        self.setupUi(self)
        self.hishorytable.clearContents()

    def winshow(self):
        # 判断是否重复打开窗口
        if win32gui.FindWindow(0, "历史记录"):
            return

        # 数据库链接
        self.data_base = Database("../videos.db")
        self.lens = len(self.data_base.search())

        # 判空
        if not self.lens:
            info = QMessageBox()
            QMessageBox.information(info, "信息", "历史记录为空", QMessageBox.Ok, QMessageBox.Ok)
            return

        self.data = self.data_base.search()
        self.additem()
        self.show()

    def addbtn(self):
        self.player = QPushButton('播放')
        self.delhistory = QPushButton('删除')
        self.player.setDown(True)
        self.delhistory.setDown(True)
        self.player.setStyleSheet(
            'background-color:#ff6633;\n'
            'border-radius:5px;\n'
            'color:white;\n'
            "margin:11px;\n"
            "font-family:Microsoft YaHei UI;\n"
            "font-size:17px;\n"
            "font-weight:bold;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "border:1px solid #ff6633;\n"
            "border-radius:5px;\n"
            "font-size: 18px;\n"
            "color:white;\n"
            "}\n"
            "QPushButton:hover:pressed\n"
            "{\n"
            "border:1px solid #ff6633;\n"
            "height:17px;\n"
            "font-size: 17px\n;"
            "color:white;}")
        self.delhistory.setStyleSheet(
            'background-color:#ff6633;\n'
            'border-radius:5px;\n'
            'color:white;\n'
            "margin:11px;\n"
            "font-family:Microsoft YaHei UI;\n"
            "font-size:17px;\n"
            "font-weight:bold;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "border:1px solid #ff6633;\n"
            "border-radius:5px;\n"
            "font-size: 18px;\n"
            "color:white;\n"
            "}\n"
            "QPushButton:hover:pressed\n"
            "{\n"
            "border:1px solid #ff6633;\n"
            "height:17px;\n"
            "font-size: 17px\n;"
            "color:white;}")
        self.hishorytable.setCellWidget(self.cnt, 5, self.player)
        self.hishorytable.setCellWidget(self.cnt, 6, self.delhistory)
        # 按钮绑定事件
        self.delhistory.clicked.connect(self.delbtn)
        self.player.clicked.connect(self.playerbtn)

    def additem(self):
        self.cnt = 0
        self.hishorytable.setRowCount(self.lens)
        self.hishorytable.setColumnWidth(4, 232)
        self.hishorytable.setColumnHidden(0, True)
        for _ in self.data:
            flagadd = 0
            try:
                self.hishorytable.setItem(self.cnt, 0, QTableWidgetItem("{}".format(_[0])))
                self.hishorytable.setItem(self.cnt, 1, QTableWidgetItem("{}".format(self.cnt + 1)))
                flagadd = 1
                self.hishorytable.setItem(self.cnt, 2, QTableWidgetItem("{}".format(_[2])))
                flagadd = 2
                self.hishorytable.setItem(self.cnt, 3, QTableWidgetItem("{}".format(_[3])))
                flagadd = 3
                self.hishorytable.setItem(self.cnt, 4, QTableWidgetItem("{}".format(_[1])))
                self.addbtn()
                self.cnt += 1
            except IndexError:
                self.hishorytable.setItem(self.cnt, flagadd, QTableWidgetItem("None"))

    def delbtn(self):
        infowin = QMessageBox()
        ans = QMessageBox.information(infowin, "删除", "确认删除？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            row = self.hishorytable.selectedItems()[0].row()
            time = self.hishorytable.item(row, 4).text()
            filedir = self.hishorytable.item(row, 0).text()
            os.remove(filedir)
            self.data_base.delete_data((time,))     # 传过去的数据必须是元组
            self.hishorytable.removeRow(row)
            self.close()
            self.show()
        if ans == QMessageBox.No:
            return

    def playerbtn(self):
        global vdo_path
        self.vdos = VideoPlayer()
        row = self.hishorytable.selectedItems()[0].row()
        vdo_path = self.hishorytable.item(row, 0).text()
        self.vdos.play_run()


