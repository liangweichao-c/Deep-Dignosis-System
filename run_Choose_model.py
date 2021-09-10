from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5 import QtCore
import Choose_model
import os
from decorate import decorator_name

class run_Choose_model(QDialog, Choose_model.Ui_Dialog):
    _signal_choose_model = QtCore.pyqtSignal(object, list)
    _signal_choose_model_close = QtCore.pyqtSignal()

    def __init__(self):
        super(run_Choose_model, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.pushButton_1.clicked.connect(self.Load_net)  # 按钮事件绑定
        self.pushButton_2.clicked.connect(self.Load_model)  # 按钮事件绑定
        self.pushButton_2.setEnabled(False)
        self.directory = None
        self.flag = False

    def show0(self):
        from PyQt5.QtCore import Qt
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowFlags(flags)
        self.show()

    def closeEvent(self, event):
        if not self.flag:
            self._signal_choose_model_close.emit()

    @decorator_name
    def Load_net(self):  # 载入网络
        from run_main import run_MainWindow
        self.directory = QFileDialog.getOpenFileName(self, "选取文件", "./Save_net", "模型文件 (*.h5);;All Files (*)")[0] or self.directory
        if self.directory:
            self.lineEdit_1.setText(os.path.basename(self.directory))
            with open(self.directory.replace('h5', 'txt'), 'r') as f:
                temp_list = (f.read().split('\n'))
                self._signal_choose_model.emit(self, temp_list)
                run_MainWindow.model_type = temp_list[1].split(':')[1]
            self.pushButton_2.setEnabled(True)

    @decorator_name
    def Load_model(self):
        from tensorflow import keras
        from run_main import run_MainWindow
        from tensorflow.keras.utils import CustomObjectScope
        from SpatialPyramidPooling import SpatialPyramidPooling
        with CustomObjectScope({'SpatialPyramidPooling': SpatialPyramidPooling}):
            run_MainWindow.load_model = keras.models.load_model(self.directory)
        run_MainWindow.load_model.summary()
        run_MainWindow.load_model_name = os.path.basename(self.directory)
        QMessageBox.information(self, "注意", "导入模型成功!")
        self.flag = True
