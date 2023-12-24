from PySide6 import QtWidgets


class TestWin(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.main_win = QtWidgets.QGridLayout(self)
        self.btn = QtWidgets.QPushButton("Button")
        self.btn_2 = QtWidgets.QPushButton("Button 2")

        self.btn.setICo

        self.main_win.addWidget(self.btn)
        self.main_win.addWidget(self.btn_2)
        print(self.main_win.indexOf(self.btn_2))

        print(self.main_win.indexOf(self.btn) in [0, 1])

app = QtWidgets.QApplication()
win = TestWin()
win.show()
app.exec()