from PyQt5.QtWidgets import QDialog
import expert
import pandas as pd

class run_expert(QDialog, expert.Ui_Dialog):
    def __init__(self):
        super(run_expert, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setFixedSize(self.width(), self.height())

        def expert_d():
            score = pd.read_csv(r'./知识库2.csv', encoding='gb18030')
            e1 = self.comboBox.currentText()
            e2 = self.comboBox_2.currentText()
            e3 = self.comboBox_3.currentText()
            e4 = self.comboBox_4.currentText()
            d = {}
            for i in range(len(score)):
                if score.iloc[i, 0] in [e1, e2, e3, e4]:
                    if score.iloc[i, 1] in d:
                        d[score.iloc[i, 1]] += score.iloc[i, 2]
                    else:
                        d[score.iloc[i, 1]] = score.iloc[i, 2]
            d = sorted(list(d.items()),key=lambda d:-d[1])
            self.lineEdit.setText(str(d[0][0]))

        data = pd.read_excel(r'./知识库.xlsx').fillna('')
        c = [(sorted(set(data.iloc[:, i].values))) for i in range(4)]
        self.comboBox.addItems(c[0])
        # self.comboBox.setFixedWidth(1050)
        self.comboBox_2.addItems(c[1])
        # self.comboBox_2.setFixedWidth(900)
        self.comboBox_3.addItems(c[2])
        # self.comboBox_3.setFixedWidth(400)
        self.comboBox_4.addItems(c[3])
        # self.comboBox_4.setFixedWidth(750)
        self.pushButton.clicked.connect(expert_d)

    def show0(self):
        from PyQt5.QtCore import Qt
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowFlags(flags)
        self.show()