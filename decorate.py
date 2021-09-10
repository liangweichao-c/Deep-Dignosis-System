from functools import wraps
from PyQt5.QtWidgets import QMessageBox
import traceback

def decorator_name(f):
    @wraps(f)
    def decorated(self):
        try:
            return f(self)
        except Exception as e:
            print(traceback.print_exc())
            QMessageBox.information(self, "注意", "操作失败")

    return decorated

def decorator_name_1(f):
    @wraps(f)
    def decorated(*args):
        try:
            return f(*args)
        except Exception as e:
            print(traceback.print_exc())
            QMessageBox.information(args[1], "注意", "数据异常")

    return decorated
