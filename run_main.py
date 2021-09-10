import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import Mainwindow
from decorate import decorator_name_1
import os

class run_MainWindow(QMainWindow, Mainwindow.Ui_MainWindow):
    def __init__(self):
        super(run_MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.frame1.setVisible(False)
        self.actiondalao.triggered.connect(self.Show_Frame1)  # 展示窗口1
        self.actionopen.triggered.connect(self.Show_Frame2)  # 展示窗口2
        self.toolBar.hide()
        self.pushButton.clicked.connect(self.start)  # 连接到
        self.pushButton_1.clicked.connect(self.open_new_net) # 连接到新建网络
        self.pushButton_2.clicked.connect(self.open_open_net) # 连接到打开网络
        self.pushButton_3.clicked.connect(self.open_train_net) # 连接到训练网络
        self.pushButton_5.clicked.connect(self.open_save_net)  # 连接到训练网络
        self.pushButton_7.clicked.connect(self.open_diagnosis)  # 连接到离线诊断
        self.pushButton_8.clicked.connect(self.open_choose_model) # 连接到模型选择
        self.pushButton_9.clicked.connect(self.open_download_data) # 连接到数据下载
        self.pushButton_10.clicked.connect(self.open_expert)  # 连接到专家知识
        self.progressBar.setValue(0)
        self.pushButton_3.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.new_net = None
        self.open_net = None
        self.train_net = None
        self.diagnosis = None
        self.download_data = None
        self.choose_model = None
        self.expert = None

    def Show_Frame1(self):
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def Show_Frame2(self):
        self.frame1.setVisible(False)
        self.frame2.setVisible(True)

    def start(self):
        self.frame_10.setVisible(False)
        self.toolBar.show()

    def clear1(self):
        self.pushButton_3.setEnabled(False)
        label = [6, 7, 8, 9, 15, 17, 18, 46, 47]
        for l in label:
            eval('self.label_{}.clear()'.format(l))

    def clear2(self, label=[19, 20, 50, 52, 41, 25, 39, 27, 42, 29, 33, 31, 44]):
        for l in label:
            eval('self.label_{}.clear()'.format(l))

    def open_new_net(self):
        from run_New_net import run_New_net
        self.new_net = run_New_net()
        self.new_net.show0()
        # 连接信号
        self.new_net._signal_new_net.connect(self.new_net_getData)

    def open_open_net(self):
        from run_Open_net import run_Open_net
        if not self.open_net:
            self.open_net = run_Open_net()
        self.open_net.show0()
        # 连接信号
        self.open_net._signal_open_net.connect(self.open_net_getData)
        self.open_net._signal_open_net_close.connect(self.clear1)

    def open_train_net(self):
        from run_Train_net2 import run_Train_net
        # if not self.train_net:
        self.train_net = run_Train_net()
        self.train_net.show0()
        # 连接信号
        self.train_net._signal_train_net1.connect(self.train_net_getData1)
        self.train_net._signal_train_net2.connect(self.train_net_getData2)
        self.train_net._signal_train_net_progressBar.connect(self.train_net_getData3)

    def open_save_net(self):
        QMessageBox.information(self, "注意", "模型保存到Save_net下")

    def open_download_data(self):
        from run_Download_data import run_Download_data
        if not self.download_data:
            self.download_data = run_Download_data()
        self.download_data.show0()

    def open_choose_model(self):
        from run_Choose_model import run_Choose_model
        if not self.choose_model:
            self.choose_model = run_Choose_model()
        self.choose_model.show0()
        self.choose_model._signal_choose_model.connect(self.choose_model_getData)
        self.choose_model._signal_choose_model_close.connect(self.clear2)

    def open_diagnosis(self):
        from run_diagnosis import run_diagnosis
        if not self.diagnosis:
            self.diagnosis = run_diagnosis()
        self.diagnosis.show0()
        self.diagnosis._signal_diagnosis1.connect(self.diagnosis_getData1)
        self.diagnosis._signal_diagnosis2.connect(self.diagnosis_getData2)

    def open_expert(self):
        from run_expert import run_expert
        if not self.expert:
            self.expert = run_expert()
        self.expert.show0()

    @decorator_name_1
    def new_net_getData(self, object, parameter):
        parameter;object
        self.clear1()
        from PyQt5 import QtGui
        self.pushButton_3.setEnabled(True)
        self.label1 = [15, 6, 7, 8, 9]
        self.label2 = [14, 0, 4, 2, 5]
        for label1, num in zip(self.label1, range(5)):
            eval('self.label_{0}.setText(parameter[{1}])'.format(label1, num))
        with open(os.path.join('Save_net', self.label_15.text() + '.txt'), 'w') as f:
            for label1, label2 in zip(self.label2, self.label1):
                eval('''f.write(self.label_{0}.text() + ":" + self.label_{1}.text() + '\\n')'''.format(label1, label2))
            png = QtGui.QPixmap('./bin/固定资源/' + self.label_6.text() + '_1.png').scaled(
                self.label_17.width(),
                self.label_17.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件的长宽
            self.label_17.setPixmap(png)  # 在label控件上显示选择的图片

    @decorator_name_1
    def train_net_getData1(self, object, parameter):
        object
        import matplotlib.pyplot as plt
        from PyQt5 import QtGui
        def draw(parameter, name):
            plt.figure(figsize=(15, 8))
            plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
            plt.plot(parameter, linewidth=6, label=u"{}曲线".format(name), color='red')
            plt.legend(fontsize=35)  ##设置图例title大小
            plt.tick_params(labelsize=30)
            plt.xticks(list(range(len(parameter))), list(range(1, len(parameter) + 1)))
            ax = plt.gca()  # 获得坐标轴的句柄
            ax.spines['bottom'].set_linewidth(5)  ###设置底部坐标轴的粗细
            ax.spines['left'].set_linewidth(5)  ####设置左边坐标轴的粗细
            plt.grid(True)
            plt.savefig('./bin/可变资源/{}.png'.format(name), bbox_inches='tight', dpi=300, pad_inches=0.0)

        draw(parameter[0], 'loss')
        png_1 = QtGui.QPixmap('./bin/可变资源/loss.png').scaled(self.label_46.width(),
                                                       self.label_46.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件的长宽
        self.label_46.setPixmap(png_1)  # 在label控件上显示选择的图片
        draw(parameter[1], 'accuracy')
        png_2 = QtGui.QPixmap('./bin/可变资源/accuracy.png').scaled(self.label_18.width(),
                                                           self.label_18.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件的长宽
        self.label_18.setPixmap(png_2)  # 在label控件上显示选择的图片
        self.pushButton_5.setEnabled(True)

    def train_net_getData2(self, parameter):
        import os
        h_temp = os.listdir('./data_train')
        h = dict([h.split('-') for h in h_temp])
        string = ''
        s = 0
        for p1, p2 in parameter.items():
            string += '{}:{}\n'.format(h[str(p1)], p2 - s)
            s = p2
        self.label_47.setText(string)

    def train_net_getData3(self, parameter):
        self.progressBar.setValue(parameter)

    @decorator_name_1
    def open_net_getData(self, object, parameter):
        object
        self.clear1()
        from PyQt5 import QtGui
        self.label1 = [15, 6, 7, 8, 9]
        self.pushButton_3.setEnabled(True)
        for label1, num in zip(self.label1, range(5)):
            eval('''self.label_{0}.setText(parameter[{1}].split(':')[-1])'''.format(label1, num))
        png = QtGui.QPixmap('./bin/固定资源/' + parameter[1].split(':')[-1] + '_1.png').scaled(
            self.label_17.width(),
            self.label_17.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件的长宽
        self.label_17.setPixmap(png)  # 在label控件上显示选择的图片

    @decorator_name_1
    def choose_model_getData(self, object, parameter):
        parameter;object
        self.clear2()
        self.pushButton_7.setEnabled(True)
        self.label1 = [25, 39, 27, 42, 29, 33, 31, 44]
        self.label2 = [0, 1, 2, 3, 4, 5, 8, 6]
        for label1, label2 in zip(self.label1, self.label2):
            eval('''self.label_{0}.setText(parameter[{1}].split(':')[-1])'''.format(label1, label2))

    def diagnosis_getData1(self, parameter):
        import matplotlib.pyplot as plt
        import matplotlib
        from PyQt5 import QtGui
        self.clear2(label=[19, 20, 50, 52, 41])
        plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
        matplotlib.rcParams['axes.unicode_minus'] = False

        plt.figure(figsize=(15, 8))
        plt.plot(parameter[1], linewidth=5)
        plt.tick_params(labelsize=30)
        ax = plt.gca()  # 获得坐标轴的句柄
        ax.spines['bottom'].set_linewidth(5)  ###设置底部坐标轴的粗细
        ax.spines['left'].set_linewidth(5)  ####设置左边坐标轴的粗细
        plt.savefig('./bin/可变资源/波形.png', bbox_inches='tight', dpi=300, pad_inches=0.0)
        png_1 = QtGui.QPixmap('./bin/可变资源/波形.png').scaled(self.label_19.width(),
                                                     self.label_19.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件的长宽
        self.label_19.setPixmap(png_1)  # 在label控件上显示选择的图片

        plt.figure(figsize=(15, 8))
        hua_fft = parameter[3]
        hua_fft(parameter[0], parameter[2], 1)
        plt.xlim(0, 300)
        plt.tick_params(labelsize=30)
        ax = plt.gca()  # 获得坐标轴的句柄
        ax.spines['bottom'].set_linewidth(5)  ###设置底部坐标轴的粗细
        ax.spines['left'].set_linewidth(5)  ####设置左边坐标轴的粗细

        plt.savefig('./bin/可变资源/频谱.png', bbox_inches='tight', dpi=300, pad_inches=0.0)
        png_1 = QtGui.QPixmap('./bin/可变资源/频谱.png').scaled(self.label_50.width(),
                                                     self.label_50.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件的长宽
        self.label_50.setPixmap(png_1)  # 在label控件上显示选择的图片

        plt.figure(figsize=(15, 8))
        plt.plot(parameter[4], 'red', label='一倍频', linewidth=5)
        plt.plot(parameter[5], 'blue', label='通频', linewidth=5)
        plt.legend(fontsize=35)
        ax = plt.gca()  # 获得坐标轴的句柄
        plt.tick_params(labelsize=30)
        plt.ylim(0, max(parameter[5]) * 1.1)
        ax.spines['bottom'].set_linewidth(5)  ###设置底部坐标轴的粗细
        ax.spines['left'].set_linewidth(5)  ####设置左边坐标轴的粗细
        plt.savefig('./bin/可变资源/一倍频.png', bbox_inches='tight', dpi=300, pad_inches=0.0)
        png_1 = QtGui.QPixmap('./bin/可变资源/一倍频.png').scaled(self.label_20.width(),
                                                      self.label_20.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件的长宽
        self.label_20.setPixmap(png_1)  # 在label控件上显示选择的图片


    def diagnosis_getData2(self, parameter1, parameter2):
        self.label_41.setText(parameter1)
        result = ''
        for p in parameter2:
            with open('./bin/固定资源/{}.txt'.format(p), 'r', encoding='utf-8') as f:
                result += f.read() + '\n'
        self.label_52.setText(result)

    def closeEvent(self, event):
        sys.exit(0)

    def keyPressEvent(self, e):
        from PyQt5.QtCore import Qt
        if e.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = run_MainWindow()
    main.show()
    sys.exit(app.exec_())