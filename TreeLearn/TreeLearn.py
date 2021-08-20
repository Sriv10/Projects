import pandas as pd
import math
import itertools
import random
import time
from matplotlib import pyplot as plt
from collections import Counter

totalCount = 0
totalLeaves = 0
length = 0
end = 'Output'

class Node():
    def __init__ (self, value, entropy = 0.0, children = {}, h = 0.0):
        self.value = value
        self.children = children
        self.entropy = entropy
        self.h = h

def avgEntropy(name, data):
    data = pd.DataFrame([data[name], data[end]])
    x1, y1 = data.shape
    dict = {}
    for x in data:
        val, result = data[x]
        initial = dict.get(val, (0,0))
        initYea, initNo = initial
        if (result == "False"):
            initYea +=1
        else:
            initNo +=1

        dict[val] = (initYea,initNo)
    tempEntropy = 0
    numValues = 0
    calculated = {}
    for var in dict:
        yes, no = dict[var]
        total = yes + no
        if (yes != 0 and no != 0):
            tempEntropy+= (-yes/total) * math.log((yes/total),2)
            tempEntropy+= (-no/total) * math.log((no/total),2)
        calculated[var] = tempEntropy
        tempEntropy = 0
        numValues += (yes + no)

    finalEntropy = 0
    for var in dict:
        yes, no = dict[var]
        finalEntropy+= ((yes + no) / numValues) * (calculated[var])
    return (finalEntropy)

def infoGain(data, col):
    dem, rep = 0,0
    for x in range(0, len(data)):
        if data.iloc[x:x+1, :][end].to_string(index = False) == "True":
            dem +=1
        else:
            rep+=1
    return (h(dem / (dem + rep), rep / (rep + dem)))

def h(one,two):
    return -(one * math.log(one,2)) - (two * math.log(two,2))

def findBest(data, stored):
    choices = list(data)
    sort = []
    for ch in choices[0:len(choices) - 1]:
        sort.append((avgEntropy(ch,data), ch))
    notFound = True
    for x in range(0,len(sorted(sort))):
        if (sorted(sort)[x][1] not in stored):
            return (sorted(sort)[x])

def learn(data, stored = ["Filler"]):
    if (len(set(data[end])) == 1):
        return Node(list(data[end])[0] )
    temp = findBest(data, stored)
    f = temp[1]
    yo = infoGain(data, temp[1])
    n = Node(temp[1], temp[0], {}, yo)
    for v in set(data[f]):
        expression = '%s == "%s"' %(f,v)
        newData = (data.query(expression))
        if (len(newData) == 0):
            continue
        else:
            #print(newData)
            child = learn(newData, stored + [f])
            n.children[v] = (child)
    return n

def printTree(node, val=None, level=0):
    if val == None:
        print('\t' * level + str(node.value))

    else:
        print('\t' * level +  str(val) + " --> " + str(node.value))


    for child in node.children:
        printTree(node.children[child], child, level + 1)

def numberOfNodes(node, val = None):
    global totalCount
    if (val == None):
        totalCount+=1
    for child in node.children:
        numberOfNodes(node.children[child], child)
        totalCount+=1

    return totalCount

def numberOfLeaves(node, val = None):
    global totalLeaves
    if (len(node.children) == 0):
        totalLeaves += 1
    for child in node.children:
        numberOfLeaves(node.children[child], child)
    return totalLeaves

def recurTotal(node):
    global totalCount
    totalCount = 0
    count = numberOfNodes(node)
    if (len(node.children) == 0):
        return 0
    for n in node.children.values():
        count+=recurTotal(n)
    return count

def numberOfNonLeaves(node):
    global totalLeaves
    global totalCount
    totalLeaves = 0
    totalCount = 0
    return numberOfNodes(node) - numberOfLeaves(node)

def avgPathLength(node):
    return (recurTotal(node)) / totalLeaves

def classify(node, test, data, filter = None):
    replace = ""
    if (len(node.children) == 0):
        return node.value
    filter = str(test[node.value])
    filter = str(filter[3:].strip())
    strip = filter.split("\n")
    filter = strip[0]
    if (filter == "?"):
        replace = question(node.value, data)
        filter = replace
    return classify(node.children[filter],test,data, filter)

def runSize(size, data, question):
    count = 0
    testNum = (random.randint(size, 232 - 50))
    final = learn(data.sample(n = size))
    #final = learn(data[0:size])
    testData = question.iloc[testNum: testNum + 50]
    for x in range(0,50):
        split = str(testData.iloc[x:x+1][end]).split("\n")
        split2 = split[0].split(    )
        if (classify(final, testData.iloc[x:x+1], data) == split2[1]):
            count+=1

    return(count / 50)

def question(col, data):
    counted = (Counter(data[col]))
    for l in counted.keys():
        if (l != "?"):
            #print(l)
            return l

'''
def main():
    xcoords = []
    ycoords = []
    pureData = 0

    pureData = pd.read_csv("houseVotes84.csv")
    pureData = pureData.drop(columns=['Label'])

    votes = pd.read_csv("houseVotes84.csv")
    votes = votes.drop(columns=['Label'])

    for col in pureData.columns:
        pureData = pureData[pureData[col] != "?"]
    final = learn(pureData)
    #printTree(final)
    #print(numberOfLeaves(final))
    #print(numberOfNodes(final))
    #print(avgPathLength(final)
    
    result = 0
    for size in range(1, 180, 5):
        for x in range(0,5):
            result+= runSize(size, pureData, votes)
        ycoords.append(result / 5)
        xcoords.append(size)
        result = 0
        print(size)

    plt.plot(xcoords, ycoords)
    plt.show()
    
    
    for size in range(1, 180, 1):
        result = runSize(size, pureData, votes)
        ycoords.append(result)
        xcoords.append(size)
        print(str(size) + " " + str(result))
    
    plt.plot(xcoords, ycoords)
    plt.show()
    '''

def main():
    print("Started")
    xcoords = []
    ycoords = []
    t = time.time()
    for lens in range(11, 14):
        data = {}
        maxLen = lens
        for num in list(itertools.product([0,1], repeat = lens)):
            for x in range(maxLen):
                data["Col" + str(x)] = data.get("Col" + str(x), []) + [num[x]]
            data["Output"] = data.get("Output", []) + [str(num.count(1) % 2 == 1)]
        df = pd.DataFrame(data=data)
        final = learn(df)
        global totalCount
        totalCount = 0
        xcoords.append(lens)
        print("Length: " + str(lens) + " Number of Nodes: " + str(numberOfNodes(final)))
        t1 = time.time()
        print("Time: " + str(t1 - t))
        ycoords.append(totalCount)
    plt.plot(xcoords,ycoords)
    plt.show()


main()
