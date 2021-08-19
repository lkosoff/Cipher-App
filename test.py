def railfence(depth=0, encrypt=True):
    if encrypt:
        rows = [[] for _ in range(depth)]

         #place
        up = True
        i=0
        for letter in ("hellothere"):
            if up:
                j = i % depth
                rows[j].append(letter)
            else:
                j = depth - 1 - (i % depth)
                rows[j].append(letter)

            if ((i+1 )% depth==0):
                up = not up
                i+=1
            i+=1
            print(j)
        
        print(rows)

        outputText = "".join(["".join(lst) for lst in rows])
        print(outputText)

railfence(depth=3)
