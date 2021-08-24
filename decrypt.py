import random
import nltk 
from urllib import request
import numpy as np
from numpy.core.numeric import cross
import threading
import time
LOCK = threading.Lock()

url = "https://www.gutenberg.org/files/98/98-0.txt"
url2 = "https://www.gutenberg.org/files/2555/2555-0.txt"

response = request.urlopen(url)
trainingData = response.read().decode('utf8')
trainingData = trainingData.replace("\r", "")
trainingData = trainingData.replace("\n", " ")[2717:758468].lower()

response2 = request.urlopen(url2)
testingData = nltk.corpus.gutenberg.raw("austen-emma.txt")
testingData = testingData.replace("\r\n", " ")
testingData = testingData.replace("\n", " ")[38:2200].lower()
N = 3

#XfreqDist1 = nltk.FreqDist(nltk.ngrams(trainingData, N))
XfreqDist1 = nltk.FreqDist(nltk.ngrams(trainingData, 1))
XfreqDist2 = nltk.FreqDist(nltk.ngrams(trainingData, 2))
XfreqDist3 = nltk.FreqDist(nltk.ngrams(trainingData, 3))



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
        self.first=True

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
    
    def currentFreq(self,cipherText):
        return nltk.FreqDist(nltk.ngrams(cipherText, N))

    def getFitness(self,cipherText):

        decipheredText = self.decipher(cipherText)
        
        alphabet = [chr(num) for num in list(range(97, 123))]
        
        yfreqDist1 = nltk.FreqDist(nltk.ngrams(decipheredText, 1))
        yfreqDist2 = nltk.FreqDist(nltk.ngrams(decipheredText, 2))
        yfreqDist3 = nltk.FreqDist(nltk.ngrams(decipheredText, 3))

        a = 1
        b = 1
        c = 1

        sum2 = np.sum([np.abs(XfreqDist2.freq((i,j)) - yfreqDist2.freq((i,j))) for j in alphabet
        for i in alphabet])

        sum3 = np.sum([np.abs(XfreqDist3.freq((i, j, k)) - yfreqDist3.freq((i, j, k))) for j in alphabet
                    for i in alphabet for k in alphabet])

        #print(sum1,sum2,sum3)
        weightedSums = (b*sum2) + .1*sum3
        self.fitnessVal = 1 / (weightedSums**2)
        


    def fitness(self, cipherText):
        if self.fitnessVal == None:     
            self.fitnessVal = self.getFitness3(cipherText)

        return self.fitnessVal

    def swap(self, dist,i,j):
        temp = dist[i]
        dist[i] = dist[j]
        dist[j] = temp

    def swapFreqValues(dist, letter1, letter2, n):
        alphabet = self.get_alphabet()
        if n==1:
            i = (letter1,)
            j = (letter2,)
            self.swap(dist,i,j)
        
        if n==2:
            for l in alphabet:
                i1 = (letter1, l)
                j1 = (letter2, l)
                self.swap(dist, i1, j1)

                i2 = (l,letter1)
                j2 = (l, letter2)
                self.swap(dist, i2, j2)
        
        if n == 3:
            for l1 in alphabet:
                for l2 in alphabet:
                    p = [(l1)]

                    i1 = (letter1, l1, l2)
                    j1 = (letter2, l1, l2)
                    self.swap(dist, i1, j1)

                    i1 = (letter1, l2, l1)
                    j1 = (letter2, l2, l1)
                    self.swap(dist, i1, j1)

                    i1 = (letter1, l2, l1)
                    j1 = (letter2, l2, l1)
                    self.swap(dist, i1, j1)

                    
                
            

    def getFitness4(self,cipherText):
        decipheredText = self.decipher(cipherText)
        
        alphabet = [chr(num) for num in list(range(97, 123))]
        
        yfreqDist1 = nltk.FreqDist(nltk.ngrams(decipheredText, 1))
        yfreqDist2 = nltk.FreqDist(nltk.ngrams(decipheredText, 2))
        #yfreqDist3 = nltk.FreqDist(nltk.ngrams(decipheredText, 3))

        a = 1
        b = 1
        c = .1

        sum1 = np.sum([np.abs(XfreqDist1.freq((i,)) - yfreqDist1.freq((i,))) for i in alphabet])

        sum2 = np.sum([np.abs(XfreqDist2.freq((i,j)) - yfreqDist2.freq((i,j))) for j in alphabet
        for i in alphabet])

        sum3 = np.sum([np.abs(XfreqDist3.freq((i,j,k)) - yfreqDist3.freq((i,j,k))) for j in alphabet
                      for i in alphabet for k in alphabet])

        #print(sum1,sum2,sum3)
        weightedSums = (a*sum1) + (b*sum2) + (c*sum3)
        return 1/ (weightedSums**2)
    
    def getFitness3(self,cipherText):
        decipheredText = self.decipher(cipherText)
        
        alphabet = [chr(num) for num in list(range(97, 123))]
        
        yfreqDist1 = nltk.FreqDist(nltk.ngrams(decipheredText, 1))
        yfreqDist2 = nltk.FreqDist(nltk.ngrams(decipheredText, 2))
        yfreqDist3 = nltk.FreqDist(nltk.ngrams(decipheredText, 3))

        a = 0
        b = 1
        c = 0#.1
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
        weightedSums = (a*sum1)**2 + (b*sum2)**2 + (c*sum3)**2
        return 1/ (weightedSums)

    def adjustSums(i,j, n):
        letter1 = chr(i + 97)
        letter2 = chr(j + 97)
        letters = [letter1, letter2]
        if n ==1:
            removal = np.sum([np.abs(XfreqDist1.freq((l,)) - self.yfreqDist1.freq((l,))) for l in letters])
            swapFreqValues(self.yfreqDist1.freq, i, j)

            add = np.sum(
                [np.abs(XfreqDist1.freq((l,)) - self.yfreqDist1.freq((l,))) for l in letters])
            total = self.sum1


    def getFitness2(self, cipherText):
        decipheredText = self.decipher(cipherText)

        alphabet = [chr(num) for num in list(range(97, 123))]
        if self.first:
            self.yfreqDist1 = nltk.FreqDist(nltk.ngrams(decipheredText, 1))
            self.yfreqDist2 = nltk.FreqDist(nltk.ngrams(decipheredText, 2))
            self.yfreqDist3 = nltk.FreqDist(nltk.ngrams(decipheredText, 3))
        
        self.first = False

        a = 1
        b = 1
        c = .1

        self.sum1 = np.sum(
            [np.abs(XfreqDist1.freq((i,)) - self.yfreqDist1.freq((i,))) for i in alphabet])

        self.sum2 = np.sum([np.abs(XfreqDist2.freq((i, j)) - self.yfreqDist2.freq((i, j))) for j in alphabet
                       for i in alphabet])

        self.sum3 = np.sum([np.abs(XfreqDist3.freq((i, j, k)) - self.yfreqDist3.freq((i, j, k))) for j in alphabet
                       for i in alphabet for k in alphabet])

        #print(sum1,sum2,sum3)
        weightedSums = (a*self.sum1)**2 + (b*self.sum2)**2 + (c*self.sum3)**2
        return 1 / (weightedSums)

    def fitness2(self, cipherText):
        decipheredText = self.decipher(cipherText)
        #print(1, decipheredText)
        decryptedNgrams = set(nltk.ngrams(decipheredText, N))
        #print(2, (decryptedNgrams))
        yfreqDist = nltk.FreqDist(decryptedNgrams)

        sum1 = [yfreqDist[ngram] * np.log2(max(float(XfreqDist[ngram]), .00001))
               for ngram in set(decryptedNgrams)]

        #lst = [ngram for ngram in set(decryptedNgrams)]

        return sum(lst)

class Population:
    def __init__(self, cipherText, populationSize, mutationThreshold, totalGenerations):
        self.fitnessList = np.zeros((populationSize,))
        self.cipherText = cipherText
        self.populationSize = populationSize
        self.mutationThreshold = mutationThreshold
        self.totalGenerations = totalGenerations
        self.nBest = max(int(populationSize * .20),1)
        self.keys = [Key() for _ in range(populationSize)]
        self.generation = 0
    
    def makeFitnessList(self):
        fitnessList = np.asarray([key.fitness(self.cipherText) for key in self.keys])
        totalFitness = np.sum(fitnessList)
        normalizedList = fitnessList/totalFitness
        
        self.fitnessList = normalizedList

    def selectParent(self):
        return random.choices(self.keys, weights=self.fitnessList, k=2)
    
    def crossover(self, parent1, parent2):
        crossoverPoint = random.randint(0, 26)
        #print(crossoverPoint)
        children = []
        for (p1, p2) in [(parent1, parent2), (parent2, parent1)]:
            key1 = p1.get_alphabet()
            key2 = p2.get_alphabet()
            tmpKey = key1[:crossoverPoint] + key2[crossoverPoint:]
            children.append(self.fixKey(tmpKey, key2))

        return children[0], children[1]

    def fixKey(self,tmpKey, tmpKey2):
        #print("TEMP", tmpKey)
        newKey = []
        repeatIndex = []
        for i,letter in enumerate(tmpKey):
            if letter in newKey:
                newKey.append("_")
                repeatIndex.append(i)
            else:
                newKey.append(letter)
        j=0
        for letter in tmpKey2:
            if letter not in newKey:
                newKey[repeatIndex[j]] = letter
                j+=1
        keyAlphabet = "".join(newKey)
        return Key(alphabet=keyAlphabet)

    def mutate(self, parent1,parent2):
        mask = np.random.randint(0, high=2, size=(26,))
        children = []
        for (p1, p2) in [(parent1, parent2), (parent2, parent1)]:
            key1 = p1.get_alphabet()
            key2 = p2.get_alphabet()
            p1_index = 0
            p2_index = 0
            tmpKey = []
            for i in mask:
                if i == 1:
                    tmpKey.append(key1[p1_index])
                    p1_index +=1
                else:
                    tmpKey.append(key2[p2_index])
                    p2_index +=1

            children.append(self.fixKey(tmpKey, key2))

        return children[0], children[1]
        

    def createChilden(self,parent1,parent2):
        
        child1,child2 = self.crossover(parent1,parent2)

        if random.random() < self.mutationThreshold:
            child1, child2 = self.mutate(child1, child2)
        return child1, child2

    def createNChildren(self,n):
        tmp =[]
        for _ in range(n):
            parent1, parent2 = self.selectParent()
            child1, child2 = self.createChilden(parent1, parent2)
            tmp.append(child1)
            tmp.append(child2)

        with LOCK:
                self.newPopulation += tmp
                

    def nextGeneration(self):
        #Initizalize new population with the top keys
        self.makeFitnessList()
        self.newPopulation = self.getBest()
        numOfThreads = 1
        n = int(self.populationSize/numOfThreads)
        threads = [threading.Thread(target=self.createNChildren, args=(n,), daemon=True)
            for _ in range(numOfThreads)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        



        self.keys = self.newPopulation
    
    def getBest(self):
        keyFitness = list(enumerate(self.fitnessList))
        keyFitness.sort(key=lambda x: x[1], reverse=True)
        return [self.keys[i] for (i, _) in keyFitness[:self.nBest]]

    def run(self):
        run = True
        while run:
            for g in range(self.totalGenerations):
                
                
                

                print("-"*10)
                print(f"Generation:{self.generation},N:{len(self.keys)}")
                if g % 1 == 0:
                    bestKey = self.getBest()[0]
                    average = np.mean([key.fitness(self.cipherText)
                                    for key in self.keys])
                    print(f"Best Key:{bestKey.get_alphabet()}")
                    print(f"Decryption:{bestKey.decipher(self.cipherText)}")
                    print(
                        f"Fitness:{bestKey.fitness(self.cipherText)}, Average:{average}")
                print("-"*10)

                self.nextGeneration()
                self.generation+=1
            x = input("Keep running?")
            if x=="no":
                break


class Solve2:
    def __init__(self, cipherText, populationSize, mutationThreshold, totalGenerations):
        self.fitnessList = np.zeros((populationSize,))
        self.cipherText = cipherText
        self.populationSize = populationSize
        self.mutationThreshold = mutationThreshold
        self.totalGenerations = totalGenerations
        self.nBest = max(int(populationSize * .20), 1)
        self.keys = [Key() for _ in range(populationSize)]
        self.generation = 0
        self.maxSwaps = 26
        self.swapPairs = [(i, j) for i in range(26) for j in range(26)]

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
        print("-"*10)
        print("-"*10)
        print(f"Generation:{i}, Max Swaps {self.maxSwaps}")
        if i % 1 == 0:
            print(f"Best Key:{self.bestKey.get_alphabet()} from iteration {keyChange}")
            print(f"Decryption:{self.bestKey.decipher(self.cipherText)}")
            print(
                f"Fitness:{self.bestKey.fitness(self.cipherText)}")
        print("-"*10)



    def solve2(self):

        self.bestKey = Key()
        self.topKeys = []
        self.bestFitness = self.bestKey.fitness(self.cipherText)
        keyChange = 0
        while True:
            for i in range(self.totalGenerations):
                tmpKey = self.makeTmpKey(self.bestKey)
                tmpKeyFitness = tmpKey.fitness(self.cipherText)

                if self.bestFitness < tmpKeyFitness:
                    self.bestKey = tmpKey
                    self.bestFitness = tmpKeyFitness
                    keyChange = i

                self.showProgess(i,keyChange)
            x = input("Keep running?")
            if x == "no":
                break
                i

  

    def solve(self):
        initialKeys = [Key() for _ in range(self.populationSize)] 
        
        self.topKeys = [(key, key.fitness(self.cipherText)) for key in initialKeys]
        self.bestKey = self.topKeys[0][0]
        
        keyChange = 0
        while True:
            for i in range(self.totalGenerations):
                tmpKeys = [self.makeTmpKey(key) for key,_ in self.topKeys]
                keyList = self.topKeys
                keyList = self.topKeys + [(key, key.fitness(self.cipherText)) for key in tmpKeys]
                keyList.sort(key=lambda x: x[1], reverse=True)

                self.topKeys = keyList[:self.populationSize]
                if self.bestKey.fitness(self.cipherText) < self.topKeys[0][1]:
                    self.bestKey = self.topKeys[0][0]
                    keyChange = i
                
                self.generation += 1
                #time.sleep(1)
                print("BEST,", self.bestKey.get_alphabet())
                print([(key.get_alphabet(),fit) for key,fit in keyList])
                
                
                self.showProgess(i, keyChange)
            
            x = input("Keep running?")
            if x == "no":
                break




        
            
        

s = Key(alphabet="abcdjfghieklmnopqrsvutwxyz")

c = s.encipher(testingData)

#p = Population(c,5,.2,1000)
#p.run()

p = Solve2(c,1,.2,6000)
p.solve()






