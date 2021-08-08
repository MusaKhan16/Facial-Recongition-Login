import PyQt5, sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from Facial_Recognition import Face_Client
from BlurWindow.blurWindow import blur
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit
from PyQt5.QtGui import QFont, QIcon, QPixmap

class MainWindow(QWidget):
    def __init__(self, width, height, window_title):
        super(MainWindow, self).__init__()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle(window_title)
        self.Main_UI()
        self.showMaximized()

        self.objectName = "MainWindow"
        self.setStyleSheet(stylesheet())
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showFullScreen()
        hWnd = self.winId()
        blur(hWnd)

        self.FaceClient = Face_Client('Ditto')

    def closeEvent(self, event):
        event.ignore()

    def Main_UI(self):
        self.Main_Frame = QWidget(self)
        self.Title()
        # self.Button()

    def Title(self):
        self.photo = QPixmap(".Assets/Face_basic.png")
        self.Logo = QtWidgets.QLabel(self, objectName = "Main-Logo")
        self.Logo.setPixmap(self.photo)
        self.Logo.resize(self.photo.width(), self.photo.height())
        self.Logo.adjustSize()
        self.Logo.move(860,185)

        self.text = QtWidgets.QLabel(self, objectName="Main-Text")
        self.text.setText("Welcome. Please sign in.")
        self.text.setFont(QFont("Century Gothic", 23))
        self.text.adjustSize()

        self.text.move(640,345)
        self.text.adjustSize()

    def Button(self):
        self.userbox = QLineEdit("Password", self, objectName="Input")
        self.userbox.setFont(QFont("Century Gothic", 18))
        self.userbox.move(650, 430)
        self.userbox.resize(350,50)

        self.button = QPushButton("Login", self, objectName="Button")
        self.button.setFont(QFont("Century Gothic", 20))
        self.button.resize(200,70)
        self.button.move(650, 500)
        
def stylesheet():
    with open(".Styles/Login.qss", "r") as file:
        return file.read()

def main():
    application = QApplication(sys.argv)
    window_insance = MainWindow(1920, 1080, "Welcome.")
    window_insance.show()
    application.setStyleSheet(stylesheet())
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
