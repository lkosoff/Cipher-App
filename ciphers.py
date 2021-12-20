import string


def letterToBinary(letter):

    num = letterToNum(letter)
    bits = []
    for _ in range(5):
        bits = [num % 2] + bits
        num = int(num/2)
    return bits

def nameToNum(name):
    lst = ["Atbash",
           "Caesar",
           "Rail Fence",
           "Vigenere",
           "Baconian"
           ]
    return lst.index(name)


def binaryToLetter(byte):
    print(byte)
    num = 0
    
    for i in range(1,len(byte)+1):
        b = byte[-i]
        num+= b * (2**(i-1))


    return numToLetter(int(num))

def letterToNum(letter):
    if letter in string.ascii_lowercase:
        return ord(letter)  - 97

    if letter in string.ascii_uppercase:
        return ord(letter) - 65
    else:
        return -1
def numToLetter(num):
    return string.ascii_lowercase[num]
class Cipher:
    def __init__ (self, inputText):
       self.alphabet = "abcdefghijklmnopqrstuvwxyz "
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

        if cipherNum == nameToNum("Vigenere"):
            self.vigenereEncrypt(keyword=options, encrypt = True)
        
        if cipherNum == nameToNum("Baconian"):
            self.baconianEncrypt(key=options)
    
    def decrypt(self, cipherNum, options):
        if cipherNum == nameToNum("Atbash"):
            self.atbash()

        if cipherNum == nameToNum("Caesar"):
            self.caesar(offset=options,encrypt=False)

        if cipherNum == nameToNum("Rail Fence"):
            self.railfenceDecrypt(depth=options)

        if cipherNum == nameToNum("Vigenere"):
            self.vigenere(keyword=options, encrypt=False)
        
        if cipherNum == nameToNum("Baconian"):
            self.baconianDecrypt(key=options)

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
    
    def railfenceDecrypt(self, depth = 0):
        slotLength = len(self.inputText)
        slots = ["" for _ in range(slotLength)]
        
        cycle = (2 * (depth - 1), 0)
        i = [0,0]
        row = 0
        turn = 0
        for letter in enumerate(self.inputText):
    
            turn = (turn + 1 ) % 2
            pos = row + (i[0] * cycle[0]) + (i[1] * cycle[1])
            print(f"{row} + ({i[0]} * {cycle[0]}) + ({i[1]} * {cycle[1]})",pos)
            if pos >= slotLength:
                i = [0, 0]
                row += 1
                turn = 0
                cycle = (cycle[0] - 2, cycle[1] + 2)
                slots[row] = letter[1]

            else:
                slots[pos] = letter[1]
                
            if row == 0:
                i[0] += 1
            elif row == depth - 1:
                    i[1] += 1
            else:
                
                i[turn] +=1
        
            print(slots, pos)
        
        self.outputText =  "".join(slots)
                
    def vigenereEncrypt(self,keyword = "a", encrypt=True):
        c = -1

        if encrypt: 
            c = 1
        
        keywordLen = len(keyword)
        output = ""
        i=0

        for letter in self.inputText:
            if letter in string.ascii_letters:
                offsetLetter = keyword[i%keywordLen]
                offset = letterToNum(offsetLetter)
                newLetterNum = (letterToNum(letter) + (c * offset)) % 27
                newLetter = numToLetter(newLetterNum)
                output += newLetter
                i += 1
        
        self.outputText = output
    

    def baconianEncrypt(self, key=("a","b")):
        lst = []
        for letter in self.inputText:
            if letter in string.ascii_letters:
                lst += letterToBinary(letter)

        output = ""
        for digit in lst:
            output+=key[digit]

        self.outputText = output

    def baconianDecrypt(self, key=("a", "b")):
        output = ""
        fiveDigits = []
        i = 0
        for letter in self.inputText:
            digit = 0
            if letter == key[0]:
                digit = 0

            if letter == key[1]:
                digit = 1
            
            fiveDigits.append(digit)
            i += 1

            if i == 5:
                print("five", fiveDigits)
                output += binaryToLetter(fiveDigits)
                fiveDigits = []
                i=0
            
            
        
        print()
        self.outputText = output
