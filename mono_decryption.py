import random
import nltk 
from urllib import request
import numpy as np
import threading
import multiprocessing
import time

event = threading.Event()

url = "https://www.gutenberg.org/files/98/98-0.txt"
url2 = "https://www.gutenberg.org/files/2555/2555-0.txt"

response = request.urlopen(url)
trainingData = response.read().decode('utf8')
trainingData = trainingData.replace("\r", "")
trainingData = trainingData.replace("\n", " ")[2717:758468].lower()

#XfreqDist1 = nltk.FreqDist(nltk.ngrams(trainingData, N))
XfreqDist1 = nltk.FreqDist(nltk.ngrams(trainingData, 1))
XfreqDist2 = nltk.FreqDist(nltk.ngrams(trainingData, 2))
XfreqDist3 = nltk.FreqDist(nltk.ngrams(trainingData, 3))

ALPHABET = [chr(num) for num in list(range(97, 123))]
UNIGRAMS = [(i, ) for i in ALPHABET]
UNIGRAM_RANGE = [i for i in range(26)]
BIGRAMS = [(i, j) for j in ALPHABET for i in ALPHABET]
BIGRAM_RANGE = [i for i in range(26 * 26)]
TRIGRAMS = [(i, j, k) for k in ALPHABET for j in ALPHABET for i in ALPHABET]
TRIGRAM_RANGE = [i for i in range(26 * 26 * 26)]
class Key:
    def __init__(self, alphabet = None):
        plainText = list(range(97, 123))
        if alphabet == None:
            cipherText = list(range(97, 123))
            random.shuffle(cipherText)
            self.alphabet = None

        else:
            cipherText = [ord(letter) for letter in alphabet]
            self.alphabet = alphabet

        self.encryptKey = dict([((plainText[i]), (cipherText[i])) for i in range(26)])
        self.decryptKey = dict([((cipherText[i]), (plainText[i]))
                          for i in range(26)])

        self.fitnessVal = None
        self.vectNgramFitness = np.vectorize(self.ngramFitness)

    def get_alphabet(self):
        if self.alphabet != None:
            return self.alphabet

        alphabet = ""
        for x in self.encryptKey.values():
            alphabet += chr(x)

        return alphabet

    def encipher(self, plaintext):
        return plaintext.translate(self.encryptKey)

    def decipher(self, plaintext):
        return plaintext.translate(self.decryptKey)
    

    def fitness(self, cipherText, weights):
        if self.fitnessVal == None:     
            self.fitnessVal = self.setFitness(cipherText,weights)

        return self.fitnessVal

    def setFitness(self, cipherText, weights):
        decipheredText = self.decipher(cipherText)
        a, b, c = weights

        sum1 = 0
        sum2 = 0
        sum3 = 0

        if a != 0:
            yfreqDist1 = nltk.FreqDist(nltk.ngrams(decipheredText, 1))
            sum1 = np.sum(self.vectNgramFitness(UNIGRAM_RANGE, 1,
                                                XfreqDist1,
                                                yfreqDist1
                                                ))

        if b != 0:
            yfreqDist2 = nltk.FreqDist(nltk.ngrams(decipheredText, 2))
            sum2 = np.sum(self.vectNgramFitness( BIGRAM_RANGE,2,
                                                XfreqDist2,
                                                yfreqDist2
                                                ))

        if c != 0:
            yfreqDist3 = nltk.FreqDist(nltk.ngrams(decipheredText, 3))
            sum3 = np.sum(self.vectNgramFitness(TRIGRAM_RANGE, 3,
                                                XfreqDist3,
                                                yfreqDist3
                                                ))

        print(sum1,sum2,sum3)
        weightedSums = max((a*sum1)**2 + (b*sum2)**2 +
                           (c*sum3)**2, .000000000001)
        return 1 / (weightedSums)

    def setFitness2(self, cipherText, weights):
        decipheredText = self.decipher(cipherText)
        
        alphabet = ALPHABET
        yfreqDist1 = nltk.FreqDist(nltk.ngrams(decipheredText, 1))
        yfreqDist2 = nltk.FreqDist(nltk.ngrams(decipheredText, 2))
        yfreqDist3 = nltk.FreqDist(nltk.ngrams(decipheredText, 3))
        
        a,b,c = weights

        sum1 = 0
        sum2 = 0
        sum3 = 0

        if a != 0:
            sum1 = np.sum([np.abs(XfreqDist1.freq((i,)) - yfreqDist1.freq((i,))) for i in alphabet])
        
        if b != 0:
            sum2 = np.sum([np.abs(XfreqDist2.freq((i,j)) - yfreqDist2.freq((i,j))) for j in alphabet
                        for i in alphabet])

        if c != 0:
            sum3 = np.sum([np.abs(XfreqDist3.freq((i,j,k)) - yfreqDist3.freq((i,j,k))) for j in alphabet
                      for i in alphabet for k in alphabet])

        #print(sum1,sum2,sum3)
        weightedSums = max((a*sum1)**2 + (b*sum2)**2 + (c*sum3)**2, .000000000001)
        return 1/ (weightedSums)


    def ngramFitness(self,i,n, xfreqDist, yfreqDist):
        if n==1:
            ngrams=UNIGRAMS
        if n == 2:
            ngrams = BIGRAMS
        if n == 3:
            ngrams = TRIGRAMS

        
        return np.abs(xfreqDist.freq(tuple(ngrams[i])) - yfreqDist.freq(tuple(ngrams[i])))

            




class Mono_Decryption:
    def __init__(self, cipherText, populationSize, totalGenerations, weights, signal):
        self.fitnessList = np.zeros((populationSize,))
        self.cipherText = cipherText
        self.populationSize = populationSize
        self.totalGenerations = totalGenerations

        self.keys = [Key() for _ in range(populationSize)]
        self.generation = 0
        self.maxSwaps = 26
        self.swapPairs = [(i, j) for i in range(26) for j in range(26)]
        self.weights = weights
        self.signal = signal
        self.decryptionHalt = threading.Event()
        
    
    def getSwaps(self):
        if self.generation % 300 == 0:
            self.maxSwaps-=1

        self.maxSwaps = max(self.maxSwaps,3)
        numOfSwaps = np.random.randint(0, high=self.maxSwaps)
        shuffledSwaps = np.random.permutation(self.swapPairs)
        return shuffledSwaps[:numOfSwaps]

    def swap(self,arr, i,j):
        tmp = arr[i]
        arr[i] = arr[j]
        arr[j] = tmp


    def makeTmpKey(self, templateKey):
        arr = list(templateKey.get_alphabet())
        swaps = self.getSwaps()
        for i,j in swaps:
            self.swap(arr,i,j)
        
        return Key(alphabet = "".join(arr))

    def showProgess(self,i,keyChange):
        
        if i == keyChange:
            self.signal.show_decryption(self.bestKey.decipher(self.cipherText))
            self.signal.show_key(self.bestKey.get_alphabet())

        self.signal.show_iterations(i, keyChange)

        print("-"*10)
        print("-"*10)
        print(f"Generation:{i}, Max Swaps {self.maxSwaps}")
        if i % 1 == 0:
            print(
                f"Best Key:{self.bestKey.get_alphabet()} from iteration {keyChange}")
            print(f"Decryption:{self.bestKey.decipher(self.cipherText)}")
            print(
                f"Fitness:{self.bestKey.fitness(self.cipherText,self.weights)}")
        print("-"*10)


    def solve2(self):

        self.bestKey = Key()
        self.topKeys = []
        self.bestFitness = self.bestKey.fitness(self.cipherText,self.weights)
        keyChange = 0
        while True:
            for i in range(self.totalGenerations):
                tmpKey = self.makeTmpKey(self.bestKey)
                tmpKeyFitness = tmpKey.fitness(self.cipherText,self.weights)

                if self.bestFitness < tmpKeyFitness:
                    self.bestKey = tmpKey
                    self.bestFitness = tmpKeyFitness
                    keyChange = i

                self.showProgess(i,keyChange)
            

    def runDecryption(self):
        print("HERE2")

        initialKeys = [Key() for _ in range(self.populationSize)] 
        
        self.topKeys = [(key, key.fitness(self.cipherText,self.weights)) for key in initialKeys]
        self.bestKey = self.topKeys[0][0]
        
        keyChange = 0
        
        for i in range(self.totalGenerations):
            if self.decryptionHalt.isSet():
                break

            tmpKeys = [self.makeTmpKey(key) for key,_ in self.topKeys]
            keyList = self.topKeys
            keyList = self.topKeys + [(key, key.fitness(self.cipherText,self.weights)) for key in tmpKeys]
            keyList.sort(key=lambda x: x[1], reverse=True)

            self.topKeys = keyList[:self.populationSize]
            if self.bestKey.fitness(self.cipherText,self.weights) < self.topKeys[0][1]:
                self.bestKey = self.topKeys[0][0]
                keyChange = i
            
            self.generation += 1
            #time.sleep(1)
            print("BEST,", self.bestKey.get_alphabet())
            print([(key.get_alphabet(),fit) for key,fit in keyList])
            
            self.showProgess(i, keyChange)

    
    def run(self):
        self.decryptThread = threading.Thread(target=self.runDecryption, args=(), daemon=True)
        self.decryptThread.start()
            
    
    
    def halt(self):
        self.decryptionHalt.set()
        self.decryptThread.join()
        self.decryptionHalt.clear()
        self.isRunning = False
        

        

            

