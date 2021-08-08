from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
import sys
from database import *
import os
from File_manager.Manager import FileManager
import pathlib
import hashlib
from popup import show_popup


class Register_window(QWidget):
    def __init__(self, width, height, title):
        super(Register_window, self).__init__()
        self.setFixedSize(width, height)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("gear.png"))
        self.setStyleSheet(stylesheet())
        self.Main_UI()

    def Main_UI(self):
        self.heading()
        self.add_file_button()
        self.password_box()
        self.configure_user()

    def heading(self):
        self.heading = QLabel("Register", self)
        self.heading.move(
            round(self.width() // 2 - 50), round(self.height() // 2.5 - 150)
        )
        self.heading.setFont(QFont("Century Gothic", 20))
        self.heading.adjustSize()

    def add_file_button(self):
        self.text_box = QPushButton("Add Photo", self, objectName="add-file-button")
        self.text_box.setGeometry(
            int(self.width() // 2 - 75), int(self.height() // 2 - 100), 200, 40
        )
        self.text_box.clicked.connect(self.add_file)

    def add_file(self):
        self.dialog = QFileDialog()
        self.folder_path = self.dialog.getOpenFileNames(
            None, "Select File", filter="Image (*.jpg, *.png)"
        )
        if not self.folder_path[0]:
            self.show_popup("Please select an image.")
            return
        root = pathlib.Path("know_faces")
        FileManager.make_dir(root, os.getlogin())
        dest = FileManager.get_dir(root, os.getlogin())
        files = FileManager.convert_to_path_object(self.folder_path[0])
        FileManager.write_dir(dest, files)

    def password_box(self):
        self.pass_box = QLineEdit(self, objectName="password-box")
        self.pass_box.setEchoMode(QLineEdit.Password)
        self.pass_box.setPlaceholderText("password")
        self.pass_box.setGeometry(
            int(self.width() // 2) - 100, int(self.height() // 2), 250, 40
        )

    def configure_user(self):
        self.text_box = QPushButton("Register", self, objectName="register-box")
        self.text_box.setGeometry(
            int(self.width() // 2 - 75), int(self.height() // 1.5), 200, 40
        )
        self.text_box.clicked.connect(self.insert)

    def show_popup(self, message):
        box = QMessageBox()
        box.setText(message)
        box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        x = box.exec_()

    def insert(self):
        password = self.pass_box.text()
        if not password:
            self.show_popup("Please enter the password.")
            return
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        insert_to_db(os.getlogin(), hashed_password)
        get_password(hashed_password)


def stylesheet():
    stylesheet_path = "styles/style.qss"
    with open(stylesheet_path, "r") as file:
        return file.read()


def main():
    app = QApplication(sys.argv)
    window_instance = Register_window(600, 600, "Configure User")
    window_instance.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
