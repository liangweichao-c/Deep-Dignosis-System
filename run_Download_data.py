from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtCore
import Download_data
import os
from decorate import decorator_name

class run_Download_data(QDialog, Download_data.Ui_Dialog):
    _signal_Download_data = QtCore.pyqtSignal(list)
    def __init__(self):
        super(run_Download_data, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setFixedSize(self.width(), self.height())
        self.pushButton_1.clicked.connect(self.connectDB)
        self.pushButton_2.clicked.connect(self.showdata)
        self.pushButton_3.clicked.connect(self.loaddata)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.client = None

    def show0(self):
        from PyQt5.QtCore import Qt
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowFlags(flags)
        self.show()

    @decorator_name
    def connectDB(self):
        from influxdb import InfluxDBClient
        self.client = InfluxDBClient(host=str(self.lineEdit.text()),
                                     port=self.lineEdit_2.text(),
                                     username=str(self.lineEdit_3.text()),
                                     password=str(self.lineEdit_4.text()),
                                     database=str(self.lineEdit_5.text()))
        InfluxDBClient.ping(self.client)
        QMessageBox.information(self, "注意", "成功连接数据库!")
        self.label_6.setText("数据库连接成功")
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)

    @decorator_name
    def load(self):
        import datetime
        time = self.dateTimeEdit.text()
        T = datetime.datetime.strptime(time, '%Y/%m/%d %H:%M')
        start = T.strftime('%Y-%m-%dT%H:%M:00Z')

        time = self.dateTimeEdit_2.text()
        T = datetime.datetime.strptime(time, '%Y/%m/%d %H:%M')
        end = T.strftime('%Y-%m-%dT%H:%M:00Z')

        point_id = self.lineEdit_6.text()
        sql = "SELECT unit_id, point_id, txt from vibra where time > '{}' and time < '{}' and point_id = '{}'".format(
            start, end, point_id)
        res = self.client.query(sql)
        res = res.get_points()
        return res

    @decorator_name
    def showdata(self):
        res = self.load()
        QMessageBox.information(self, "注意", "这段时间内一共有{}条数据！".format(len(list(res))))

    @decorator_name
    def loaddata(self):
        import pandas as pd
        time = self.dateTimeEdit.text()
        res = self.load()
        logdir = os.path.join("vibra")
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        data = []
        for r in res:
            data.extend(list(map(float, r['txt'].split('|'))) + [''])
            time = r['time'].replace(':', '_').replace('T', ' ').replace('Z', '')
        pd.DataFrame(data).to_csv(os.path.join(r'./vibra', '{}_{}.csv'.format(time, r['point_id'])), header=False, index=False)
        QMessageBox.information(self, "注意", "成功下载数据!\n请在根目录vibra文件夹中查看")