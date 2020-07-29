

import operator
import gensim
import logging
from gensim.models import Word2Vec
import time
import pandas as pd 


def createBasketsFile():
    startTime = time.time()
    basketsDf = pd.DataFrame(columns = ['item1','item1Desc','item2','item2Desc','item3','item3Desc','item3Occurences','item3Dist'])    
    i1 = 0
    index = 0
    for item in mostconsumedItems[:300]:
        basket = []
        item = str(item)
        if (not isItemValid(item)):
            continue
        basket.append(item)
        i1 = i1 + 1
        i2 = i1 
        for item2 in mostconsumedItems[i2:300]:
            item2 = str(item2)
            if (not isItemValid(item)):                
                continue            
            basket.append(item2)
            i2 = i2 + 1
            
            for item3withScore in model.predict_output_word(basket):
                item3 = item3withScore[0]
                if (isItemValid(item3) and (item3 not in basket)):                                               
                    basketsDf.at[index, 'item1'] = item
                    basketsDf.at[index, 'item1Desc'] =  desc(item)
                    basketsDf.at[index, 'item2'] = item2
                    basketsDf.at[index, 'item2Desc'] = desc(item2)
                    basketsDf.at[index, 'item3'] = item3
                    basketsDf.at[index, 'item3Desc'] = desc(item3)
                    basketsDf.at[index, 'item3Occurences'] = itemsOccurencesDic[str(item3)]
                    basketsDf.at[index, 'item3Dist'] = item3withScore[1]
                    index = index + 1
                    break                    
            basket.remove(item2)

        if (i1 % 10 == 0):
            print (i1)
    endTime = time.time()
    print ("total time:", endTime - startTime)
    basketsDf.to_excel("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\selectedBaskets.xlsx")


def allPermutations():
    allStartTime = time.time()
    gradesPerBasket = pd.DataFrame(columns = ['basket', 'grade']) 
    for item in mostconsumedItems:
        basket = []
        basket.append(item)
        i1 = i1 + 1
        i2 = i1 
        for item2 in mostconsumedItems[i2:]:
            basket.append(item2)
            i2 = i2 + 1
            i3 = i2
            for item3 in mostconsumedItems[i3:]:
                i3 = i3 + 1
                basket.append(item3)

                startTime = time.time()            
                grade = CalculateBasketTotalGrade(basket,allTransactions)            
                gradesPerBasket["basket"] = basket
                gradesPerBasket["grade"] = grade

                gradesPerBasket = gradesPerBasket.sort_values(by=['grade'])[:30]
            
                endTime = time.time()
                print ("totalTime:" ,endTime - startTime,  " basket:",basket," grade:", grade)

                basket.remove(item3)
            basket.remove(item2)
    allEndTime = time.time()
    print("total time for all:", allEndTime - allStartTime)


def desc(w1):
    try:
        if (pd.isnull(itemsWithDescription[str(w1)])):
            return str(w1)
        return itemsWithDescription[str(w1)].replace(' ','')
    except: 
        return str(w1)

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

def isItemValid(itemId):
    itemHierarchy = getHierarchy(itemId)
    if (itemHierarchy == '4900.0' or itemHierarchy == '0.0' or itemHierarchy == '7000.0' or itemId == '2' or itemHierarchy == '4900' or itemHierarchy == '7000' or itemHierarchy == '0'):
        return False
    return True

model = Word2Vec.load("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Model\\wfm_80.model")

dfitemsDesc = pd.read_csv("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\ItemsDescriptions.csv")
itemsWithDescription = dfitemsDesc.set_index('ItemId').to_dict()['ItemDescription']

clusters =  pd.read_excel("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\clustersDataFrame.xlsx")
clustersSorted = clusters.sort_values('TotalOccurences', ascending=False)
mostconsumedItems = clustersSorted["item1Id"]

dfitems = pd.read_csv("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\\Items\\AllItemsWithoutDuplicate.csv")
itemsWithHierarchy = dfitems.set_index('ItemId').to_dict()['FinancialHierarchy']


dfitemsOccurences =  pd.read_csv("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\\Items\ItemsOccurences_80.csv")
itemsOccurencesDic = dfitemsOccurences.set_index('ItemId').to_dict()['Occurences']

createBasketsFile()