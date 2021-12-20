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

key1 = Key()
print(key1.encipher("A"))



class Mono_Decryption_Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Title Here')
        uic.loadUi('ui_files/mono.ui', self)
        self.options = None

        self.connectInputs()
        self.decryptButton_mono.clicked.connect(self.runDecryption)
        self.decryptCurrent.clicked.connect(
            lambda: self.runDecryption(useCurrentKey=True))
        self.haltButton.clicked.connect(self.halt)
        
        self.settingsFrame.setVisible(False)
        self.settingsButton.clicked.connect(
            lambda: self.settingsFrame.setVisible(not self.settingsFrame.isVisible()))

        self.mono_decryption = None
        self.isMonoRunning = False

        self.keyWidget = KeyWidget()
        self.keyWidget.keyEdited.connect(self.manualKeyChange)
        self.keyBox.layout().insertWidget(0, self.keyWidget)

    def connectSlidersAndSpinBox(self, widget, val):
        widget.setValue(val)

    def connectInputs(self):
        inputs = [(self.populationSizeSlider, self.populationInput),
                  (self.swapsSlider, self.swapsInput),
                  (self.unigramSlider, self.unigramInput),
                  (self.bigramSlider, self.bigramInput),
                  (self.trigramSlider, self.trigramInput)]

        self.populationSizeSlider.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.populationInput, val))

        self.populationInput.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.populationSizeSlider, val))

        self.swapsSlider.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.swapsInput, val))

        self.swapsInput.valueChanged.connect(
            lambda val: self.connectSlidersAndSpinBox(self.swapsSlider, val))

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


    def runDecryption(self, useCurrentKey=False):
        if not self.isMonoRunning:
            self.isMonoRunning = True
            signal = Signal(display=self.showDecryption, generation=self.showIterations,
                            showKey=self.showKey, swapVal=self.swapsInput.setValue)

            cipherText = self.cipherText_mono.toPlainText()
            populationSize = self.populationInput.value()
            maxSwaps = self.swapsInput.value()
            weights = (self.unigramInput.value(),
                       self.bigramInput.value(), self.trigramInput.value())

            self.mono_decryption = Mono_Decryption(
                cipherText, populationSize, maxSwaps, weights, signal)

            customKey = None

            if useCurrentKey:
                alphabetArr, missing_letter = self.keyWidget.getCipherAlphabet()
                if missing_letter != []:
                    return
                customKey = "".join(alphabetArr)

            self.mono_decryption.run(customKey)

    def showDecryption(self, passed_string):
        self.plainText_mono.setPlainText(passed_string)

    def showIterations(self, passed_tuple):
        current_i, last_i = passed_tuple
        self.generationNum.display(current_i)
        self.lastChangeNum.display(last_i)

    def showKey(self, passed_string):
        self.keyWidget.showKeyPlainText(passed_string)

    def halt(self):
        if self.mono_decryption != None and self.isMonoRunning:
            self.mono_decryption.halt()
            self.isMonoRunning = False

    def manualKeyChange(self, newKey):
        key = Key(alphabet=newKey)
        d = key.decipher(self.cipherText_mono.toPlainText())
        self.showDecryption(d)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = cipherApp()
    widget.show()
    sys.exit(app.exec())
