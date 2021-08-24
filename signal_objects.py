
from PyQt6.QtCore import QObject, pyqtSignal

class Signal(QObject):
    """
    This is a QObject which communicates with the 
    twitter_account_welcome_controller and sends a string
    to the feed
    """

    #The signal that gets sent between classes
    decryptData = pyqtSignal(str)
    decryptData2 = pyqtSignal(tuple)
    decryptData3 = pyqtSignal(str)


    def __init__(self, display, generation,showKey):
        """
        Takes a function that updates the feed
        """
        super().__init__()

        self.decryptData.connect(display)
        self.decryptData2.connect(generation)
        self.decryptData3.connect(showKey)

    def show_decryption(self, message):
        """
        This function emits a signal carrying a string
        which will get outputted to the feed
        """
        self.decryptData.emit(message)
    
    def show_iterations(self, current_i, last_i):
        self.decryptData2.emit((current_i, last_i))
    
    def show_key(self, key_alphabet):
        self.decryptData3.emit(key_alphabet)

