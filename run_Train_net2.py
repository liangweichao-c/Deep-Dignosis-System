from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSlot
import Train_net
from tensorflow import keras
from decorate import decorator_name


class PrintLogs(QThread, keras.callbacks.Callback):
    signal_epoch_begin = QtCore.pyqtSignal(float)
    def on_train_begin(self, logs=None):
        print('欢迎你，张家盛')

    def on_epoch_begin(self, epoch, logs={}):
        self.epochs = self.params.get('epochs')
        time = (float(epoch) / float(self.epochs) * 100)
        self.signal_epoch_begin.emit(time)
        print('time', time)

    def on_train_end(self, logs=None):
        self.signal_epoch_begin.emit(100)
        print('再见，张家盛')

class MyThread(QThread): # 建立一个任务线程类
    signal_training = QtCore.pyqtSignal(float) #设置触发信号传递的参数数据类型,这里是浮点
    signal_train_end = QtCore.pyqtSignal()  # 设置触发信号传递的参数数据类型
    signal_train_net_train_stop = QtCore.pyqtSignal()
    signal_load_data_end = QtCore.pyqtSignal()  # 设置触发信号传递的参数数据类型
    signal_fail = QtCore.pyqtSignal(int)

    def __init__(self, object, flag):
        super(MyThread, self).__init__()
        self.run_train_net = object
        self.flag = flag
        self.printlogs = PrintLogs()
        self.printlogs.signal_epoch_begin.connect(self.show_epoch_begin)

    def run(self): # 在启动线程后任务从这个函数里面开始执行
        try:
            if self.flag == 1:
                self.run_train_net.train()
                self.signal_train_end.emit()
            elif self.flag == 0:
                self.run_train_net.Load_data2()
                self.signal_load_data_end.emit()
        except:
            self.signal_fail.emit(self.flag)

    def show_epoch_begin(self, i):
        self.signal_training.emit(i)

class run_Train_net(QDialog, Train_net.Ui_Dialog):
    _signal_train_net1 = QtCore.pyqtSignal(object, list)
    _signal_train_net2 = QtCore.pyqtSignal(dict)
    _signal_train_net_progressBar = QtCore.pyqtSignal(float)


    def __init__(self):
        super(run_Train_net, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setFixedSize(self.width(), self.height())
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.comboBox_3.currentIndexChanged.connect(self.opti)

    # @decorator_name
    @pyqtSlot()
    def on_pushButton_1_clicked(self):  # 导入数据1
        if self.radioButton_1.isChecked() == True:
            pass

    @pyqtSlot()
    def on_pushButton_2_clicked(self): # 导入数据2
        self.pushButton_2.setEnabled(False)
        self.mythread = MyThread(self, 0)  # 实例化自己建立的任务线程类
        self.mythread.signal_load_data_end.connect(self.load_data_end)
        self.mythread.signal_fail.connect(self.fail)
        self.mythread.start()

    @pyqtSlot()
    def on_pushButton_3_clicked(self): # 开始训练
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(True)
        self.mythread = MyThread(self, 1)  # 实例化自己建立的任务线程类
        self.mythread.signal_training.connect(self.training)  # 设置任务线程发射信号触发的函数
        self.mythread.signal_train_end.connect(self.train_end)  # 设置任务线程发射信号触发的函数
        self.mythread.signal_fail.connect(self.fail)
        self.printlogs = self.mythread.printlogs
        self.mythread.start()  # 启动任务线程

    @pyqtSlot()
    def on_pushButton_4_clicked(self): # 停止训练
        self.mythread.printlogs.model.stop_training = True
        QMessageBox.information(self, "注意", "训练停止!")
        self.pushButton_4.setEnabled(False)

    def opti(self):
        if self.comboBox_3.currentText() == '请选择优化算法' or 'self.y_train' not in vars():
            self.pushButton_3.setEnabled(False)
        else:
            self.pushButton_3.setEnabled(True)

    def load_data_end(self):
        self.pushButton_2.setEnabled(True)
        QMessageBox.information(self, "注意", "导入完成!")
        self.mythread.terminate()

    def training(self, i):
        self._signal_train_net_progressBar.emit(i)

    def train_end(self):
        self.pushButton_3.setEnabled(True)
        QMessageBox.information(self, "注意", "训练完成!")
        self.mythread.terminate()

    def fail(self, i):
        if i == 0:
            self.pushButton_2.setEnabled(True)
        elif i == 1:
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(False)
        QMessageBox.information(self, "注意", "操作失败!")
        self.mythread.terminate()

    def show0(self):
        from PyQt5.QtCore import Qt
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowFlags(flags)
        self.show()

    # @decorator_name
    def Load_data2(self):  # 导入数据2并直接处理
        from run_main import run_MainWindow
        import data_processing
        self.label_5.setText("正在载入数据，请等待...")
        DataPath = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "./")
        if run_MainWindow.model_type == '时序深度融合网络' and self.radioButton_2.isChecked()==True and DataPath:
            self.x_train_time, self.x_train_deep, self.y_train, num_dic = data_processing.data_processing(DataPath, net=run_MainWindow.model_type, is_train=True)
            self._signal_train_net2.emit(num_dic)
            print(self.x_train_time.shape, self.x_train_deep.shape, self.y_train.shape)

        elif self.radioButton_2.isChecked()==True and DataPath:
            self.x_train, self.y_train, num_dic = data_processing.data_processing(DataPath, net=run_MainWindow.model_type, is_train=True)
            self._signal_train_net2.emit(num_dic)
            print(self.x_train.shape,self.y_train.shape)
        else:
            raise ValueError

        if self.y_train.shape != (0,) and DataPath:
            self.label_5.setText("数据数目:{}条".format(self.y_train.shape))
        else:
            raise ValueError

    # @decorator_name
    def train(self):
        import os
        from tensorflow import keras
        # import keras
        import tensorflow.compat.v1 as tf
        from run_main import run_MainWindow
        logdir = os.path.join("Save_net")
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        output_model_file = os.path.join(logdir, run_MainWindow.model_name)
        output_model_file = output_model_file + '.h5' if '.h5' not in output_model_file else output_model_file
        print(output_model_file)
        with open(output_model_file.replace('h5', 'txt'), 'a+') as f:
            if len(f.read().split('\n')) <= 8:
                f.write('{}:{}\n'.format(self.label_8.text(), self.comboBox_3.currentText()))
                f.write('{}:{}\n'.format(self.label_10.text(), self.doubleSpinBox_3.value()))
                f.write('{}:{}\n'.format(self.label_9.text(), self.doubleSpinBox_2.value()))
                f.write('{}:{}\n'.format(self.label_11.text(), self.doubleSpinBox_5.value()))


        if run_MainWindow.model_type == '时序深度融合网络':
            x, y = [self.x_train_time,self.x_train_deep], self.y_train
        else:
            x, y = self.x_train, self.y_train
        callbacks = [
            keras.callbacks.TensorBoard(logdir),
            keras.callbacks.ModelCheckpoint(output_model_file, save_weights_only=False
                                            # ,save_best_only=True      #有验证集才可以用这个 沃日
                                            ),
            keras.callbacks.EarlyStopping(patience=5, min_delta=self.doubleSpinBox_2.value()),
            self.printlogs,
        ]
        # 模型训练参数

        with run_MainWindow.graph.as_default():
            tf.keras.backend.set_session(run_MainWindow.session)
            run_MainWindow.model.compile(loss="sparse_categorical_crossentropy",
                          optimizer=self.comboBox_3.currentText(),
                          metrics=["acc"])

        # 开始训练！
            history = run_MainWindow.model.fit(x, y,
                                               batch_size=int(self.doubleSpinBox_3.value()),
                                               epochs=int(self.doubleSpinBox_5.value()),
                                               verbose=1,
                                               callbacks=callbacks)  # validation_data=(x_valid, y_valid),

        self._signal_train_net1.emit(self, list(history.history.values()))