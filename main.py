from signal_objects import Signal
import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QStackedWidget, QWidget, QMainWindow, QComboBox, QListWidget
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from keyWidget import KeyWidget
from cipher_controller import Cipher_Controller
from ciphers import Cipher
from mono_decryption_controller import Mono_Decryption_Controller, Key
from steganography_controller import Steganography_Controller
from text_steganography_controller import Text_Steganography_Controller
import string


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Title Here')
        uic.loadUi('ui_files/main_window.ui', self)

        self.sidebar.clicked.connect(self.setWindow)
        
        self.mainStack.addWidget(Cipher_Controller())
        self.mainStack.addWidget(Mono_Decryption_Controller())
        self.mainStack.addWidget(Steganography_Controller())
        self.mainStack.addWidget(Text_Steganography_Controller())



    def setWindow(self, passed):
        self.mainStack.setCurrentIndex(passed.row())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainApp()
    widget.show()
    sys.exit(app.exec())
