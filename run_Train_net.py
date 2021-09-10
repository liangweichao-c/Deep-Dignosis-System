from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtCore, QtWidgets
import Train_net
from decorate import decorator_name


class run_Train_net(QDialog, Train_net.Ui_Dialog):
    _signal_train_net1 = QtCore.pyqtSignal(object, list)
    _signal_train_net2 = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(run_Train_net, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setFixedSize(self.width(), self.height())
        self.pushButton_1.clicked.connect(self.Load_data1)
        self.pushButton_2.clicked.connect(self.Load_data2)
        self.pushButton_3.clicked.connect(self.train)
        self.pushButton_3.setEnabled(False)

    def show0(self):
        from PyQt5.QtCore import Qt
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowFlags(flags)
        self.show()

    def Load_data1(self):  # 导入数据1
        global data
        if self.radioButton_1.isChecked()==True:
            pass

    @decorator_name
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
        else:return

        if self.y_train.shape != (0,):
            self.label_5.setText("数据数目:{}条".format(self.y_train.shape))
            QMessageBox.information(self, "注意", "数据载入成功!")
            self.pushButton_3.setEnabled(True)
        else:
            raise ValueError

    @decorator_name
    def train(self):
        import os
        from tensorflow import keras
        import pandas as pd
        from run_main import run_MainWindow
        # from Printlogs import PrintLogs
        logdir = os.path.join("Save_net")
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        output_model_file = os.path.join(logdir, run_MainWindow.model_name)
        output_model_file = output_model_file + '.h5' if '.h5' not in output_model_file else output_model_file
        print(output_model_file)
        # 模型训练参数
        run_MainWindow.model.compile(loss="sparse_categorical_crossentropy",
                      optimizer=self.comboBox_3.currentText(),
                      metrics=["acc"])
        callbacks = [
            keras.callbacks.TensorBoard(logdir),
            keras.callbacks.ModelCheckpoint(output_model_file, save_weights_only=False
                                            # ,save_best_only=True      #有验证集才可以用这个 沃日
                                            ),
            keras.callbacks.EarlyStopping(patience=5, min_delta=self.doubleSpinBox_2.value()),
            # PrintLogs(),
        ]
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
        # 开始训练！
        history = run_MainWindow.model.fit(x, y,
                                           batch_size=int(self.doubleSpinBox_3.value()),
                                           epochs=int(self.doubleSpinBox_5.value()),
                                           verbose=1,
                                           callbacks=callbacks)  # validation_data=(x_valid, y_valid),
        QMessageBox.information(self, "注意", "训练完成!")
        self._signal_train_net1.emit(self, list(history.history.values()))