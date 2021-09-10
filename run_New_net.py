from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtCore
import New_net
from decorate import decorator_name


class run_New_net(QDialog, New_net.Ui_Dialog):
    _signal_new_net = QtCore.pyqtSignal(object, list)

    def __init__(self):
        super(run_New_net, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setFixedSize(self.width(), self.height())
        self.pushButton.clicked.connect(self.new)  # 按钮事件绑定
        self.pushButton.setEnabled(False)
        self.comboBox_1.currentIndexChanged.connect(self.Model_Shape)
        self.flag = False

    def show0(self):
        from PyQt5.QtCore import Qt
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowFlags(flags)
        self.show()

    @decorator_name
    def Model_Shape(self):
        if self.comboBox_1.currentText() == '请选择网络':
            self.pushButton.setEnabled(False)
            self.lineEdit_2.setText('')
            return
        else:
            self.pushButton.setEnabled(True)

        self.lineEdit_2.setText(self.comboBox_1.currentText())

        if self.comboBox_1.currentText() != '请选择网络':
            self.pushButton.setEnabled(True)

    @decorator_name
    def new(self):
        assert len(self.lineEdit_1.text()) > 0

        from tensorflow import keras
        from run_main import run_MainWindow
        # import tensorflow as tf
        import tensorflow.compat.v1 as tf

        data_str = []
        data_str.append(self.lineEdit_1.text())
        data_str.append(self.lineEdit_2.text())
        data_str.append(self.comboBox_2.currentText())
        data_str.append(self.lineEdit_5.text())
        data_str.append(self.lineEdit_3.text())
        # 发送信号
        self._signal_new_net.emit(self, data_str)
        tf.disable_eager_execution()
        run_MainWindow.graph = tf.get_default_graph()
        run_MainWindow.session = tf.Session()
        tf.keras.backend.set_session(run_MainWindow.session)

        if self.comboBox_1.currentText() == 'CNN网络':
            from Model_CNN import Model_CNN_body
            input = keras.layers.Input(shape=(128, 128, 1))
            output = Model_CNN_body(input)
            run_MainWindow.model = keras.models.Model(inputs=[input],
                                                      outputs=[output])  # 模型搭建

        elif self.comboBox_1.currentText() == 'SPP网络':
            from Model_PSPP import Model_PSPP_body
            input = keras.layers.Input(shape=(None, None, 1))
            output = Model_PSPP_body(input)
            run_MainWindow.model = keras.models.Model(inputs=[input],
                                   outputs=[output])  # 模型搭建

        elif self.comboBox_1.currentText() == '时序深度融合网络':
            from Model_Time_Deep import Model_Time_Deep_body
            input_time = keras.layers.Input(shape=(None, 1))
            input_deep = keras.layers.Input(shape=(128, 128, 1))
            output = Model_Time_Deep_body(input_time,input_deep)
            run_MainWindow.model = keras.models.Model(inputs=[input_time,input_deep],
                                                      outputs=[output])  # 模型搭建


        run_MainWindow.model.summary()

        run_MainWindow.model_name = self.lineEdit_1.text()
        run_MainWindow.model_type = self.lineEdit_2.text()
        # 展示网络信息

        QMessageBox.information(self, "注意", "新建网络成功!")
        self.flag = True