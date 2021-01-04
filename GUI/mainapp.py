# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QDesktopWidget
from PyQt5.QtGui import QIcon
import sys


class MainApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(1000, 780)
        self.resize(1200, 880)
        self.center()
        self.setWindowTitle('Tello Drone App')
        self.setWindowIcon(QIcon('web.png'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                    "Are you sure you want to quit?", QMessageBox.Yes |
                                    QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():

    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
