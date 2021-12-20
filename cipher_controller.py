from signal_objects import Signal
import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QStackedWidget, QWidget, QMainWindow, QComboBox, QSpinBox, QSlider
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from keyWidget import KeyWidget
import ciphers
from ciphers import Cipher
from mono_decryption import Mono_Decryption, Key
import string
from cipherUiForm import Ui_Form


class Cipher_Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Title Here')
        #uic.loadUi('ui_files/ciphers.ui', self)s

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.options = None

        self.ui.encryptButton.clicked.connect(self.encryptText)
        self.ui.decryptButton.clicked.connect(self.decryptText)
        self.ui.backButton.clicked.connect(lambda : self.ui.optionStack.setCurrentIndex(0))
        self.ui.cipherList.clicked.connect(self.setOptionsWindow)

    def encryptText(self):
        """
        Converts plain text text encrypted text
        """
        text = self.ui.inputText.toPlainText()
        cipherNum = self.ui.cipherList.currentIndex().row()
        self.getOptions(cipherNum)

        cipher = Cipher(text)
        cipher.encrypt(cipherNum, self.options)
        self.ui.outputText.setPlainText(
            cipher.getOutput(removeSpacing=self.ui.removeSpacingButton.isChecked()))

    def decryptText(self):
        """
        Converts encrypted text to plain text
        """
        text = self.ui.inputText.toPlainText()
        cipherNum = self.ui.cipherList.currentIndex().row()
        self.getOptions(cipherNum)

        cipher = Cipher(text)
        cipher.decrypt(cipherNum, self.options)

        self.ui.outputText.setPlainText(cipher.getOutput())

    def setOptionsWindow(self, index):
        #q = QStackedWidget().set
        print(dir(index))
        self.ui.cipherName.setText(index.data())
        self.ui.optionStack.setCurrentIndex(1)
        self.ui.optionsPage.setCurrentIndex(index.row())

    def getOptions(self, index):
        #Caesar Cipher
        if index == 1:
            self.options = self.ui.caesarOffset.value()
            print("SET", self.options)
        #railfence
        if index == 2:
            self.options = self.ui.railfenceDepth.value()

        #vigenere
        if index == 3:
            self.options = self.ui.vigenereKeyword.text()
        
        #baconian
        if index == 4:
            self.options = (self.ui.baconianFirst.text(), self.ui.baconianSecond.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainApp()
    widget.show()
    sys.exit(app.exec())
