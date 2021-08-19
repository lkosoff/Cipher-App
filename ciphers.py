def nameToNum(name):
    lst = ["Atbash",
           "Caesar",
           "Rail Fence"
           ]
    return lst.index(name)


class Cipher:
    def __init__ (self, inputText):
       self.alphabet = "abcdefghijklmnopqrstuvwxyz"
       self.inputText = inputText.lower()
       self.outputText = ""
       

    def getOutput(self, removeSpacing = False):
        
        if removeSpacing:
            newOutput = ""
            for letter in self.outputText:
                if letter!=" ":
                    newOutput += letter

            return newOutput

        return self.outputText

    def encrypt(self,cipherNum, options):
        print(f"options{options}")
        if cipherNum == nameToNum("Atbash"):
            self.atbash()
        
        if cipherNum == nameToNum("Caesar"):
            self.caesar(offset=options,encrypt=True)
        
        if cipherNum == nameToNum("Rail Fence"):
            self.railfence(depth=options, encrypt=True)

    
    def decrypt(self, cipherNum, options):
        if cipherNum == nameToNum("Atbash"):
            self.atbash()

        if cipherNum == nameToNum("Caesar"):
            self.caesar(offset=options,encrypt=False)
    
    def _getAlphabetPos(self, letter):
        """
        Gets the index of lowercase letters
        """
        return ord(letter)  - 97

    def atbash(self):
        """
        Reverses the alphabet. Z=A, Y=B, X=C etc..
        """
    
        outputText = ""
        for letter in self.inputText:
            if letter in self.alphabet:
                i = self._getAlphabetPos(letter)
                outputText += self.alphabet[-i - 1 ]
            
            else:
                outputText += letter
        
        self.outputText = outputText
        

    def caesar(self, offset=0, encrypt=True):
      
        factor = -1
        if encrypt:
            factor = 1
        
        outputText = ""
        for letter in self.inputText:
            if letter in self.alphabet:
                i = self._getAlphabetPos(letter)
                new_i = ((factor * offset) + i) % 26
                print(i,new_i,f"offset{offset}")
                outputText += self.alphabet[new_i]

            else:
                outputText += letter

        self.outputText = outputText
        print(self.outputText)

    def railfence(self, depth=0, encrypt=True):
        if encrypt:
            rows = [[] for _ in range(depth)]

            #place
            up = True
            i = 0
            for letter in self.inputText:
                if letter == " ":
                    continue
                if up:
                    j = i % depth
                    rows[j].append(letter)
                else:
                    j = depth - 1 - (i % depth)
                    rows[j].append(letter)

                if ((i+1) % depth == 0):
                    up = not up
                    i += 1
                i += 1
                
                
            #Join rows together
            self.outputText = "".join(["".join(lst) for lst in rows])
        else:
            slots = ["" for _ in range(len(self.inputText))]

            for letter in self.inputText:
                
        
