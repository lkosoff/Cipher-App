import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QStackedWidget, QWidget, QMainWindow, QFileDialog, QGraphicsView
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtCore, uic
import os
from steganography import encodeImage,decodeImage


class Steganography_Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Steganography')
        uic.loadUi('ui_files/steganography.ui', self)
        
        self.decrypt_select_image_button.clicked.connect(
            lambda: self.getImage("decode"))

        self.encrypt_select_image_button.clicked.connect(
            lambda: self.getImage("encode"))
        
        self.sidebar.clicked.connect(
            lambda i: self.stackWindow.setCurrentIndex(i.row()))

        self.decodeImageButton.clicked.connect(self.decode)
        self.saveEncodedImage.clicked.connect(self.saveEncodedFile)
        self.filename = {"encode":"", "decode":""}

    def getFile(self):
        filters = "Image files (*.jpg *.gif *.png *jpeg)"
        response = QFileDialog.getOpenFileName(
            parent=self, caption="Select File", directory=os.getcwd() , filter=filters)

        return response
    
    def saveEncodedFile(self):
        if self.filename["encode"] != "":
            saveFile , _ = QFileDialog.getSaveFileName(self, "Save Image", directory=os.getcwd(), filter="Image files (*.png)")
            msg = self.encodeMessageInput.toPlainText()
            encodeImage(self.filename["encode"],saveFile, msg)
        
    

    def getImage(self, option):
        filename = self.getFile()[0]
        if filename != "":
            if option == "encode":
                self.filename[option] = filename
                pathDisplay = self.encrypt_upload_path
                imageDisplay = self.encryptImage
                w = self.encryptImageBox.width()
            
            if option == "decode":
                self.filename[option] = filename
                pathDisplay = self.decrypt_upload_path
                imageDisplay = self.decryptImage
                w = self.decryptImageBox.width()
                
            
            pathDisplay.setText(self.filename[option])
            h = w
            
            imageDisplay.setPixmap(
                QPixmap(
                    self.filename[option]).scaled(
                    w,
                    h,
                    aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    transformMode=QtCore.Qt.TransformationMode.FastTransformation))

    def decode(self):
        if self.filename["decode"] != "":
            msg = decodeImage(self.filename["decode"])
            self.decodeMessageOutput.setPlainText(msg)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Steganography_Controller()
    widget.show()
    sys.exit(app.exec())
