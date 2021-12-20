
from PyQt6.QtCore import QObject, pyqtSignal

class Signal(QObject):
    """
    This is a QObject which communicates with the 
    twitter_account_welcome_controller and sends a string
    to the feed
    """

    #The signal that gets sent between classes
    decryptText = pyqtSignal(str)
    generationDisplay = pyqtSignal(tuple)
    keyDisplay = pyqtSignal(str)
    swapDisplay = pyqtSignal(int)


    def __init__(self, display, generation,showKey,swapVal):
        """
        Takes a function that updates the feed
        """
        super().__init__()

        self.decryptText.connect(display)
        self.generationDisplay.connect(generation)
        self.keyDisplay.connect(showKey)
        self.swapDisplay.connect(swapVal)

    def show_decryption(self, message):
        """
        This function emits a signal carrying a string
        which will get outputted to the feed
        """
        self.decryptText.emit(message)
    
    def show_iterations(self, current_i, last_i):
        self.generationDisplay.emit((current_i, last_i))
    
    def show_key(self, key_alphabet):
        self.keyDisplay.emit(key_alphabet)

    def updateSwaps(self, swapNum):
        self.swapDisplay.emit(swapNum)

