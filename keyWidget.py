from output import Ui_Form
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtGui import QIcon
import string
from mono_decryption import Key
from PyQt6.QtCore import QObject, pyqtSignal

class KeyWidget(QWidget):
    keyEdited = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        ui = Ui_Form()
        ui.setupUi(self)
        self.ui = ui
        

        self.key_display = [ui.a_key, ui.b_key, ui.c_key,
                            ui.d_key, ui.e_key, ui.f_key,
                            ui.g_key, ui.h_key, ui.i_key,
                            ui.j_key, ui.k_key, ui.l_key,
                            ui.m_key, ui.n_key, ui.o_key,
                            ui.p_key, ui.q_key, ui.r_key,
                            ui.s_key, ui.t_key, ui.u_key,
                            ui.v_key, ui.w_key, ui.x_key,
                            ui.y_key, ui.z_key]

        for key in self.key_display:
            key.textEdited.connect(self.keyEdit)
        
        for display in self.ui.main_frame.children():
            if isinstance(display, QLineEdit):
                display.setStyleSheet(
                    "background-color:rgb(80, 96, 118);\nborder-style: double;\nborder-width: 1px;\nborder-radius: 10px;\nborder-color: rgb(200,200,200);\ntext-align: center;\ncolor: rgb(200,200,200);")
        self.showingMissingLetters = False
        #self.key = Key(alphabet=string.ascii_lowercase)
        

    def keyEdit(self, passed_string):
        #print("P", passed_string)
        if passed_string in string.ascii_letters and passed_string != "":

            alphabetArr, missing_letters = self.getCipherAlphabet()
            if missing_letters == []:
                cipherAlphabet = "".join(alphabetArr)
                self.keyEdited.emit(cipherAlphabet)
                print(cipherAlphabet)


            #key = Key(alphabet=self.getCipherAlphabet())
            #d = key.decipher(self.cipherText_mono.toPlainText())
            #self.showDecryption(d)
    
    def showKeyPlainText(self, cipherKey):
        for i, letter in enumerate(cipherKey):
            j = ord(letter) - 97
            display = self.key_display[j]
            plainTextLetter = chr(i+97)
            display.setText(plainTextLetter.upper())

    def getCipherAlphabet(self):
        
        alphabetArr = ["_" for _ in range(26)]

        positions = [[] for _ in range(26)]
        missing_letter = []
    


        for i, display in enumerate(self.key_display):
            rawText = display.text()
            display.setText(rawText.upper())
            txt = rawText.lower()
        
            pos = ord(txt) - 97
            
            cipherTextLetter = chr(i+97)
            positions[pos].append(i)
            cipherTextLetter = chr(i+97)
            alphabetArr[pos] = cipherTextLetter
        
        for i, p in enumerate(positions):
            if p == []:
                missing_letter.append(chr(i+97).upper())
            
            elif len(p) > 1:
                for j in p:
                    self.key_display[j].setStyleSheet("color:rgb(255,154,160)")
            
            else:
                #print(p)
                j = p[0]
                self.key_display[j].setStyleSheet(
                    "color:rgb(230,230,230)")
        
        
        
        print(missing_letter)


        
        if self.showingMissingLetters:
            self.missing_letters_label.deleteLater()
            self.showingMissingLetters = False

        if missing_letter != []:
            self.missing_letters_label = QLabel()
            self.showingMissingLetters = True
            self.missing_letters_label.setText(f"Missing Letters: {missing_letter}")
            self.missing_letters_label.setWordWrap(True)
            self.missing_letters_label.setStyleSheet("color:rgb(255,154,160)")
             

            self.ui.main_frame.layout().addWidget(self.missing_letters_label)

        return alphabetArr, missing_letter
            

        
#instantiate app
"""app = QApplication(sys.argv)

w = KeyWidget()
w.showKeyPlainText("xyzabcdefghijklmnopqrstuvw")
w.show()


sys.exit(app.exec())
"""
