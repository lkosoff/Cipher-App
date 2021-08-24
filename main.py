from signal_objects import Signal
import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QStackedWidget, QWidget, QMainWindow,QComboBox, QSpinBox, QSlider
from PyQt6.QtGui import QIcon
from PyQt6 import uic
import ciphers
from ciphers import Cipher
from mono_decryption import Mono_Decryption


#a = QSlider().valueChanged.connect()
class cipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Title Here')
        uic.loadUi('ui_files/main_window.ui', self)
        self.options = None


        self.encryptButton.clicked.connect(self.encryptText)
        self.decryptButton.clicked.connect(self.decryptText)
        self.cipherSelection.activated.connect(self.setOptionsWindow)

        self.connectInputs()
        self.decryptButton_mono.clicked.connect(self.runDecryption)
        self.haltButton.clicked.connect(self.halt)
        self.mono_decryption = None
        self.isMonoRunning = False


    def connectSlidersAndSpinBox(self,widget, val):
        widget.setValue(val)

    
    def connectInputs(self):
        inputs = [(self.populationSizeSlider, self.populationInput),
                  (self.iterationsSlider, self.iterationsInput),
                  (self.unigramSlider, self.unigramInput),
                  (self.bigramSlider, self.bigramInput),
                  (self.trigramSlider, self.trigramInput)]

        self.populationSizeSlider.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.populationInput, val))
    
        self.populationInput.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.populationSizeSlider, val))
            
        self.iterationsSlider.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.iterationsInput, val))

        self.iterationsInput.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.iterationsSlider, val))

        self.unigramSlider.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.unigramInput, val/100))

        self.unigramInput.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.unigramSlider, val*100))

        self.bigramSlider.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.bigramInput, val/100))

        self.bigramInput.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.bigramSlider, int(val*100)))

        self.trigramSlider.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.trigramInput, val/100))

        self.trigramInput.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.trigramSlider, val*100))

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
            
    def runDecryption(self):
        if not self.isMonoRunning:
            self.isMonoRunning = True
            print("HERE1")
            signal = Signal(display=self.showDecryption, generation=self.showIterations,showKey=self.showKey)

            cipherText = self.cipherText_mono.toPlainText()
            populationSize = self.populationInput.value()
            totalGenerations = self.iterationsInput.value()
            weights = (self.unigramInput.value(), self.bigramInput.value(), self.trigramInput.value())
            self.mono_decryption = Mono_Decryption(cipherText,populationSize,totalGenerations, weights, signal)
            self.mono_decryption.run()
        
    def showDecryption(self, passed_string):
        self.plainText_mono.setPlainText(passed_string)
    
    def showIterations(self, passed_tuple):
        current_i, last_i = passed_tuple
        self.generationNum.display(current_i)
        self.lastChangeNum.display(last_i)
    
    def showKey(self, passed_string):
        key_display = [self.a_key, self.b_key, self.c_key,
         self.d_key, self.e_key, self.f_key,
         self.g_key, self.h_key, self.i_key,
         self.j_key, self.k_key, self.l_key,
         self.m_key, self.n_key, self.o_key,
         self.p_key, self.q_key, self.r_key,
         self.s_key, self.t_key, self.u_key,
         self.v_key, self.w_key, self.x_key,
         self.y_key, self.z_key]

        for i, display in enumerate(key_display):
            display.setText(passed_string[i].upper())
    
    def halt(self):
        if self.mono_decryption != None and self.isMonoRunning:
            self.mono_decryption.halt()
            self.isMonoRunning = False

    def manualKeyChange():
        pass
        #QLineEdit().

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = cipherApp()
    widget.show()
    sys.exit(app.exec())
