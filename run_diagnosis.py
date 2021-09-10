from PyQt5.QtWidgets import QDialog
import diagnosis
from PyQt5 import QtCore
from decorate import decorator_name

class run_diagnosis(QDialog, diagnosis.Ui_Dialog):
    _signal_diagnosis1 = QtCore.pyqtSignal(list)
    _signal_diagnosis2 = QtCore.pyqtSignal(str, list)
    def __init__(self):
        super(run_diagnosis, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.retranslateUi(self)
        self.pushButton.clicked.connect(self.Load_test_data)
        self.pushButton_2.clicked.connect(self.Diagnosis1)
        self.pushButton_2.setEnabled(False)

    def show0(self):
        from PyQt5.QtCore import Qt
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowFlags(flags)
        self.show()

    @decorator_name
    def Load_test_data(self):
        from PyQt5 import QtWidgets
        import numpy as np
        import os
        import data_processing
        self.label.setText("正在载入数据，请等待...")
        TestDataPath = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "./")


        from run_main import run_MainWindow
        if run_MainWindow.model_type == '时序深度融合网络' and TestDataPath:
            for file in os.listdir(TestDataPath):
                temp_x_time, temp_x_deep, data_str = data_processing.data_processing(os.path.join(TestDataPath, file), net=run_MainWindow.model_type, is_train=False)
                self.x_test_time = np.append(self.x_test_time, temp_x_time, axis=0) if 'self.x_test_time' in vars() else temp_x_time
                self.x_test_deep = np.append(self.x_test_deep, temp_x_deep, axis=0) if 'self.x_test_deep' in vars() else temp_x_deep

            print(self.x_test_time.shape,self.x_test_deep.shape)
        elif TestDataPath:
            for file in os.listdir(TestDataPath):
                temp_x, data_str = data_processing.data_processing(os.path.join(TestDataPath, file), net=run_MainWindow.model_type, is_train=False)
                self.x_test = np.append(self.x_test, temp_x, axis=0) if 'self.x_test' in vars() else temp_x

            print(self.x_test.shape)
        else:return
        self._signal_diagnosis1.emit(data_str)
        self.label.setText("数据载入完成！")
        self.pushButton_2.setEnabled(True)

    @decorator_name
    def Diagnosis1(self):
        import numpy as np
        import os
        from run_main import run_MainWindow
        if run_MainWindow.model_type == '时序深度融合网络':
            predict_data = run_MainWindow.load_model.predict([self.x_test_time,self.x_test_deep])
        else:
            predict_data = run_MainWindow.load_model.predict(self.x_test)
        predict_data = np.argmax(predict_data, axis=1)
        dic_num = {}
        for i in predict_data:
            dic_num[i] = dic_num[i] + 1 if i in dic_num else 1
        temp_S = ''
        result = []
        files = os.listdir('./data_train')
        dic_name = dict([file.split('-') for file in files])
        for key, value in dic_num.items():
            temp_S += '{}:{}%\n'.format(dic_name[str(key)], round(value / len(predict_data) * 100, 2))
            if value / len(predict_data) * 100 >= 40:
                result.append(dic_name[str(key)])
        self._signal_diagnosis2.emit(temp_S, result)
        self.label.setText("诊断完成！")