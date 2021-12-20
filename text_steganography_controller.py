import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QStackedWidget, QWidget, QMainWindow, QFileDialog, QGraphicsView
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtCore, uic
from textStegUiForm import Ui_Form

class Text_Steganography_Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Title Here')

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        #self.ui.customCoverTextButton.clicked.connect(lambda : self.ui.coverTextStack.setCurrentIndex(1))
    

