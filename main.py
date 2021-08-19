import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget, QMainWindow,QComboBox, QSpinBox
from PyQt6.QtGui import QIcon
from PyQt6 import uic
import ciphers
from ciphers import Cipher


#a = QSpinBox().va
class cipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Title Here')
        uic.loadUi('ui_files/main_window.ui', self)
        self.options = None

        self.encryptButton.clicked.connect(self.encryptText)
        self.decryptButton.clicked.connect(self.decryptText)
        self.cipherSelection.activated.connect(self.setOptionsWindow)
        

        

    def encryptText(self):
        """
        Converts plain text text encrypted text
        """
        text = self.inputText.toPlainText()
        cipherNum = self.cipherSelection.currentIndex()
        self.getOptions(cipherNum)

        cipher = Cipher(text)
        cipher.encrypt(cipherNum, self.options)
        self.outputText.setPlainText(
            cipher.getOutput(removeSpacing=self.removeSpacingButton.isChecked()))


    def decryptText(self):
        """
        Converts encrypted text to plain text
        """
        text = self.inputText.toPlainText()
        cipherNum = self.cipherSelection.currentIndex()
        self.getOptions(cipherNum)

        cipher = Cipher(text)
        cipher.decrypt(cipherNum,self.options)

        self.outputText.setPlainText(cipher.getOutput())

    def setOptionsWindow(self, index):
        #q = QStackedWidget().set
        self.optionsPage.setCurrentIndex(index)

    def getOptions(self, index):
        #Caesar Cipher
        if index == 1:
            self.options = self.caesarOffset.value()
            print("SET", self.options)
        #railfence
        if index==2:
            self.options = self.railfenceDepth.value()
            


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = cipherApp()
    widget.show()
    sys.exit(app.exec())
