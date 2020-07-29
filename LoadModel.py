
import pandas as pd 
import gensim
import logging
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize 
import numpy as np
import operator
#import mpld3
import sys

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE



def printList(lst):
     for line in lst:
        try:
            print(desc(line[0])," - " , line[1])
        except:
            print(line[0]," - " , line[1])

def printListSimple(lst):
     for line in lst:
        try:
            print(desc(line)," - " , line)
        except:
            print(line," - " , line)

def printListToFile(lst, fileForPrint):
     for line in lst:
        try:
            print(line[0], ",", desc(line[0]),"-" , line[1], file = fileForPrint)
        except:
            missingDescription = missingDescription + 1
            print(line[0]," - " , line[1], file = fileForPrint)

def mostSimilar(model):
    print()
    w1 = input("Please input item id: ") 
    print()
    try:
        print("----Your item", desc(w1) , "-----")
    except:
        print("----Your item", w1 , "-----")
    print()
    mostSimilar = model.wv.most_similar(positive=w1)
    printList(mostSimilar)

    
def mostLikely(model):
    numberOfClusters = 550
    numberOfItemsInCluster = 10
    similarityThreshold = 0.27
    mostConsumed  = dict(sorted(itemsOccurencesDic.items(), key=operator.itemgetter(1), reverse=True)[:numberOfClusters])
    fileForPrint = open('LoranBasket_threshold0.27.txt', 'w') 
    csvFile = open('clusters.csv', 'w')
    index = 1

    clustersDataFrame = pd.DataFrame(columns=['ClusterNumber', 'TotalOccurences'
    , 'item1Desc', 'item1Hierarchy', 'item2Desc', 'item3Desc', 'item4Desc', 'item5Desc'
    , 'item6Desc', 'item7Desc', 'item8Desc', 'item9Desc', 'item10Desc'
    , 'item1Distance', 'item2Distance', 'item3Distance', 'item4Distance', 'item5Distance'
    , 'item6Distance', 'item7Distance', 'item8Distance', 'item9Distance', 'item10Distance'
    , 'item1Occurences', 'item2Occurences', 'item3Occurences', 'item4Occurences', 'item5Occurences'
    , 'item6Occurences', 'item7Occurences', 'item8Occurences', 'item9Occurences', 'item10Occurences'
    , 'item1Id', 'item2Id', 'item3Id', 'item4Id', 'item5Id'
    , 'item6Id', 'item7Id', 'item8Id', 'item9Id', 'item10Id'])

    for item in mostConsumed.keys():        
        try:
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", file = fileForPrint)
            #print(index, "Most Consumed item",item, ', ', desc(item) , "-----")
            print(index, "Most Consumed item", file = fileForPrint)
            print(item, ',', desc(item), file = fileForPrint)
        except:
            print("Most Consumed item", item , "-----", file = fileForPrint)
        print(numberOfItemsInCluster ," most similar items are:", file = fileForPrint)
        item1Hierarchy = getHierarchy(item)

        if (item1Hierarchy == '4900.0' or item1Hierarchy == '0.0' or item1Hierarchy == '7000.0' or item == '2'):
            continue
        
        mostSimilar = model.wv.most_similar(positive=item, topn = numberOfItemsInCluster)
        mostSimilar2 = list(filter(lambda x: x[1] > similarityThreshold, mostSimilar))
        printListToFile(mostSimilar2, fileForPrint)
        item1Occurences = itemsOccurencesDic[item]
        totalOccurences = item1Occurences

        clustersDataFrame.at[index, 'ClusterNumber'] = index
        clustersDataFrame.at[index, 'item1Desc'] = desc(item)
        clustersDataFrame.at[index, 'item1Distance'] = 1
        clustersDataFrame.at[index, 'item1Id'] = item
        clustersDataFrame.at[index, 'item1Hierarchy'] = item1Hierarchy
        clustersDataFrame.at[index, 'item1Occurences'] = item1Occurences

        for i in range(2, numberOfItemsInCluster+1): #df.at[rowname, columnName]
            numberOfFilteredItems = len(mostSimilar2)
            if (i-2 >= numberOfFilteredItems):
                break
                                              
            similarItem = mostSimilar2[i-2][0]
            similarItemHierarchy = getHierarchy(similarItem)

            if (similarItemHierarchy == '4900.0' or similarItemHierarchy == '0.0' or similarItemHierarchy == '7000.0' or similarItem == '2'):
                continue
            
            clustersDataFrame.at[index, 'item'+str(i)+'Id'] = similarItem
            clustersDataFrame.at[index, 'item'+str(i)+'Desc'] = desc(similarItem)
            clustersDataFrame.at[index, 'item'+str(i)+'Distance'] = mostSimilar2[i-2][1]
            itemiOccurences = itemsOccurencesDic[similarItem]
            totalOccurences = totalOccurences + itemiOccurences
            clustersDataFrame.at[index, 'item'+str(i)+'Occurences'] = itemiOccurences

        clustersDataFrame.at[index, 'TotalOccurences'] = totalOccurences
        print('\n', file = fileForPrint)
        index = index + 1

    # print(clustersDataFrame)
    # print(clustersDataFrame, file = fileForPrint)
    clustersDataFrame.to_excel("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\\Items\\clustersDataFrame.xlsx")  
    print(". ", file = fileForPrint)
    fileForPrint.close() 
    print("number of missing descriptions are:",missingDescription)
    

def predictOuputWord(model):
    print()
    w1 = input("Please input list of item ids: ") 
    list  = w1.split(',')
    print()
    print("----Your list:", "-----")
    for id in list:
       print(desc(id))
    print()
    print("--Predict_output_word:")
    predictWord =  model.predict_output_word(list, topn=10)       
    printList(predictWord)


def desc(w1):
    w1 = w1.replace(',', '')
    try:
        if (pd.isnull(itemsWithDescription[w1])):
            missingDescription = missingDescription + 1
            return w1
        return itemsWithDescription[w1]
    except: 
        return w1

def getHierarchy(itemId):
    try:
        if (pd.isnull(itemsWithHierarchy[itemId])):            
            return '-1'
        return itemsWithHierarchy[itemId]
    except: 
        try:
            return itemsWithHierarchy[int(itemId)]
        except:
            return '-1.1'

# dfitems =  pd.read_csv("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\\Items\ItemsDict.csv")
# itemsDic = dfitems.set_index('ProductId').to_dict()['Description']

dfitems = pd.read_csv("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\\Items\\AllItemsWithoutDuplicate.csv")
itemsWithHierarchy = dfitems.set_index('ItemId').to_dict()['FinancialHierarchy']

dfitemsDesc =  pd.read_csv("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\\Items\\ItemsDescriptions.csv")
itemsWithDescription = dfitemsDesc.set_index('ItemId').to_dict()['ItemDescription']

dfitemsOccurences =  pd.read_csv("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\\Items\ItemsOccurences_80.csv")
itemsOccurencesDic = dfitemsOccurences.set_index('ItemId').to_dict()['Occurences']

model = Word2Vec.load("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Model\\wfm_80.model")
missingDescription = 0
 
for x in range(600):
    print()
    print("For mostSimilar press 1")
    print("For predictOuputWord press 2")   
    print("For Clusters press 3")
    choice = input("please input your choice --> ") 
    
    #try:
    if(choice == '1'):
        mostSimilar(model)
    if(choice == '2'):
        predictOuputWord(model)
    if (choice == '3'):
        mostLikely(model)
  
