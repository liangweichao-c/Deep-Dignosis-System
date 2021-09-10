from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5 import QtCore
import Open_net
import os
from decorate import decorator_name

class run_Open_net(QDialog, Open_net.Ui_Dialog):
    _signal_open_net = QtCore.pyqtSignal(object, list)
    _signal_open_net_close = QtCore.pyqtSignal()
    def __init__(self):
        super(run_Open_net, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setFixedSize(self.width(), self.height())
        self.pushButton_1.clicked.connect(self.Load_net)  # 按钮事件绑定
        self.pushButton_2.clicked.connect(self.Load_model)  # 按钮事件绑定
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
            self._signal_open_net_close.emit()

    @decorator_name
    def Load_net(self):  # 载入网络
        self.directory = QFileDialog.getOpenFileName(self, "选取文件", "./Save_net", "模型文件 (*.h5);;All Files (*)")[0] or self.directory
        if self.directory:
            self.lineEdit_1.setText(os.path.basename(self.directory))

            with open(self.directory.replace('h5', 'txt'), 'r') as f:
                temp_list = (f.read().split('\n'))
                self._signal_open_net.emit(self, temp_list)
                from run_main import run_MainWindow
                run_MainWindow.model_type = temp_list[1].split(':')[1]

    @decorator_name
    def Load_model(self):
        from tensorflow import keras
        # import tensorflow as tf
        from tensorflow.keras.utils import CustomObjectScope
        from SpatialPyramidPooling import SpatialPyramidPooling
        import tensorflow.compat.v1 as tf
        from run_main import run_MainWindow
        tf.disable_eager_execution()
        run_MainWindow.graph = tf.get_default_graph()
        run_MainWindow.session = tf.Session()
        tf.keras.backend.set_session(run_MainWindow.session)
        try:
            run_MainWindow.model = keras.models.load_model(self.directory)
        except:
            with CustomObjectScope({'SpatialPyramidPooling': SpatialPyramidPooling}):
                run_MainWindow.model = keras.models.load_model(self.directory)
        run_MainWindow.model.summary()
        run_MainWindow.model_name = os.path.basename(self.directory)
        # run_MainWindow.model._make_predict_function()
        QMessageBox.information(self, "注意", "导入模型成功!")
        self.flag = True
