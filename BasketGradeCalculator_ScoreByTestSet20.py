
import operator
import gensim
import logging
from gensim.models import Word2Vec
import time
import pandas as pd 


itemToHrtItems = dict()
itemsToRtItems = dict()

def CalculateGradeForBasketInTransaction(basket, transaction):
    
    basketSize = len(basket)
    grade = [0, ""];
    bingoFound = 0;
    hrtFound=0;
    rtFound = 0;
    for item in basket:              

        if item in transaction:
            grade[0]= grade[0]+(1/basketSize);
            bingoFound = bingoFound + 1;

        else:
            hrtItem = GetHrtItems(str(item));
            if (len(list(set(hrtItem) & set(transaction)))>0):
                grade[0] = grade[0]+((1/basketSize)*HRTFactor);
                hrtFound = hrtFound+1;

        #elif rtItem in transaction:
            else:
                rtItem = GetRtItems(str(item));
                if (len(list(set(rtItem) & set(transaction)))>0):
                    grade[0] = grade[0]+((1/basketSize)*RTFactor);
                    rtFound = rtFound+1


    if (grade[0] < 0.5 or bingoFound< 1 or ((bingoFound + hrtFound) < 2 and (bingoFound + rtFound) < basketSize)):
        grade[0] = 0;
    else:
        grade[1] = GetBasketInTransaction(bingoFound, hrtFound, rtFound)
    return grade;

def GetBasketInTransaction(bingoFound, hrtFound, rtFound):
    if (bingoFound == 3):
        return "BBB";
    elif (bingoFound == 2 and hrtFound == 0 and rtFound == 0):
        return "BBN"
    elif (bingoFound == 2 and hrtFound == 1):
        return "BBH"
    elif (bingoFound == 2 and rtFound == 1):
        return "BBR"
    elif (bingoFound == 1 and hrtFound == 2):
        return "BHH";
    elif(bingoFound == 1 and rtFound == 2):
        return "BRR"
    elif (bingoFound == 1 and hrtFound == 1 and rtFound ==1):
        return "BHR";
    elif (bingoFound == 1 and hrtFound == 1 and rtFound == 0):
        return "BHN";
    else:
        return "N/A"
    

def GetHrtItems(item):
    result = itemToHrtItems.get(item)
    if result is not None:
        return result
    
    itemsHrt= []
    mostSimilar = model.wv.most_similar(positive=str(item))
    for pair in mostSimilar:
        if pair[1] > HRT:
            itemsHrt.append(pair[0])
        else:
            break
    itemToHrtItems[item] = itemsHrt
    return itemsHrt;

def GetRtItems(item):
    result = itemsToRtItems.get(item)
    if result is not None:
        return result

    itemsRt= []
    mostSimilar = model.wv.most_similar(positive=str(item))
    for pair in mostSimilar:
        if pair[1] < HRT and pair[1] >RT:
            itemsRt.append(pair[0])
        else:
            break
    itemsToRtItems[item] = itemsRt
    return itemsRt;


def CalculateTransactionScore(transaction, baskets, transactionGrade, lastTime):
    basketsGrade = {}
    i=-1
    currTime = time.time()
    print ("number or baskets: " , len(baskets), " delta time:", currTime - lastTime)
    for basket in baskets:
        i = i+1
        basketsGrade[i] = CalculateGradeForBasketInTransaction(basket, transaction);

    basketWithHigherGrade = max(basketsGrade.items(), key=operator.itemgetter(1))[0];
    if basketsGrade[basketWithHigherGrade] == 0:
        return transactionGrade;

    transactionGrade = transactionGrade + basketsGrade[basketWithHigherGrade] 

    for item in baskets[basketWithHigherGrade]:
        try:
            transaction.remove(item)
        except ValueError:
            TryRemoveHrtItem(transaction, item)
        
    return CalculateTransactionScore(transaction, baskets, transactionGrade,currTime)

def TryRemoveHrtItem(transaction, item):
    itemsHrt = GetHrtItems(item);
    for item in itemsHrt:
        try:
            transaction.remove(item)
            return
        except ValueError:
            a=1
    return

fileForPrint = open('C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\LoranBasketsWithGrades.txt', 'w') 

def CalculateBasketTotalGrade(basket,transactions):
    totalGrade = [0, {"BBB": 0, "BBN": 0, "BBH": 0, "BBR" : 0, "BHH" : 0, "BRR" : 0, "BHR":0, "BHN":0} ]
    startTime = time.time()
    i = 0
    for transaction in transactions:
        currentTransactionResults = CalculateGradeForBasketInTransaction(basket, transaction)
        totalGrade[0] =  totalGrade[0] + currentTransactionResults[0]
        if currentTransactionResults[0] > 0:
            totalGrade[1][currentTransactionResults[1]] = totalGrade[1][currentTransactionResults[1]] + 1


        i = i + 1
    strForPrint = "basket" ,basket," grade:",totalGrade," total time:",time.time() - startTime    
    print (strForPrint)
    print (strForPrint, file=fileForPrint)
    
    return totalGrade 


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
                gradesPerBasket["grade"] = grade[0]

                gradesPerBasket = gradesPerBasket.sort_values(by=['grade'])[:30]
            
                endTime = time.time()
                print ("totalTime:" ,endTime - startTime,  " basket:",basket," grade:", grade)

                basket.remove(item3)
            basket.remove(item2)
    allEndTime = time.time()
    print("total time for all:", allEndTime - allStartTime)

# dfitems = pd.read_csv("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\AllItemsWithoutDuplicate.csv")
# dfitems = pd.read_csv("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\ItemsDescriptions.csv")
# itemsWithDescription = dfitems.set_index('ItemId').to_dict()['ShortDescription']
# itemsWithDescription = dfitems.set_index('ItemId').to_dict()['ItemDescription']

def description(w1):
    try:
        if (pd.isnull(itemsWithDescription[w1])):
            return w1
        return itemsWithDescription[w1]
    except: 
        return w1





#numberOfBaskets = 100

def basketsByComplementary():
    allStartTime = time.time()
    gradesPerBasket = pd.DataFrame(columns = ['basket', 'grade']) 
    basketsWithGradesDf = pd.DataFrame(columns=['BasketNumber', 'TotalBasketScore'
    , 'Item1Id', 'Item1Desc', 'Item2Id', 'Item2Desc', 'Item3Id', 'Item3Desc', 'Distance2To1', 'Distance3To1'])

    itemsCounter = 1

    for item in mostconsumedItems[:numberOfBaskets]:
        basket = []
        basket.append(str(item))
        basketsWithGradesDf.at[itemsCounter, 'BasketNumber'] = itemsCounter
        basketsWithGradesDf.at[itemsCounter, 'Item1Id'] = item
        basketsWithGradesDf.at[itemsCounter, 'Item1Desc'] = description(str(item))

        mostSimilarItemsForBasket = model.predict_output_word(basket, topn=5)
        similarItem2 =  mostSimilarItemsForBasket[0][0]
        if similarItem2 not in basket:
            basket.append(similarItem2)
            basketsWithGradesDf.at[itemsCounter, 'Item2Id'] = similarItem2
            basketsWithGradesDf.at[itemsCounter, 'Item2Desc'] = description(similarItem2)
			# basketsWithGradesDf.at[itemsCounter, 'Distance2To1'] = mostSimilarItemsForBasket[0][1]  # todo: fix this, its not the distance
        
        similarItem3 = mostSimilarItemsForBasket[1][0] 
        if similarItem3 not in basket:
            basket.append(similarItem3)
            basketsWithGradesDf.at[itemsCounter, 'Item3Id'] = similarItem3
            basketsWithGradesDf.at[itemsCounter, 'Item3Desc'] = description(similarItem3)
            # basketsWithGradesDf.at[itemsCounter, 'Distance3To1'] = mostSimilarItemsForBasket[1][1]
        
        # todo: maybe this next "if" is never used and should be deleted
        if (len(basket) < 3):
            predictWord3 = mostSimilarItemsForBasket[2][0] 
            if predictWord3 not in basket:
                basket.append(predictWord3)
            
        startTime = time.time()            
        print("basket",itemsCounter)            
        grade = CalculateBasketTotalGrade(basket,allTransactions)[0]         
        basketsWithGradesDf.at[itemsCounter, 'TotalBasketScore'] = grade
        endTime = time.time()
        gradesPerBasket["basket"] = basket
        gradesPerBasket["grade"] = grade

        #gradesPerBasket = gradesPerBasket.sort_values(by=['grade'])[:30]
        #print ("totalTime:" ,endTime - startTime,  " basket:",basket," grade:", grade)
        itemsCounter = itemsCounter + 1
                
    allEndTime = time.time()    
    gradesPerBasket.to_csv("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\basketsByComplementary.csv")
    excelFileName = "C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\" 
    # excelFileName += str(numberOfBaskets)
    excelFileName += "BasketsByMostLikely_"
    excelFileName += str(numberOfTransactions)
    excelFileName += "Trxs.xlsx"
    basketsWithGradesDf.to_excel(excelFileName)  
    print("total time for all:", allEndTime - allStartTime)
    print("total time for all:", allEndTime - allStartTime, file=fileForPrint)

#basketsFile = pd.read_excel("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\All Baskets sorted by 3rd item occurences.csv", skiprows=1)
#next(basketsFile)
#basketsDf = pd.DataFrame(basketsFile)

# basketsFile = open("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\AllBasketsSortedBy3rdItemOccurences.xlsx", "r")
basketsFile = open("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\ScoringBaskets_5772875Trxs.csv", "r")
# basketsFile = open("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\AllBasketsSortedBy3rdItemOccurences.txt", "r")
next(basketsFile)
basketsLines = basketsFile.read()


def ScoringBasketBy20():
    allStartTime = time.time()
    gradesPerBasket = pd.DataFrame(columns = ['basket', 'grade'])
    basketsWithGradesDf = pd.DataFrame(columns=['BasketNumber', 'Index', 'TotalBasketScore_80', 'Item1', 'Item1Desc', 'Item2', 'Item2Desc', 'Item3'
    , 'Item3Desc', 'item3Occurences', 'item3Dist','TotalBasketScore_20','BBB', 'BBN', 'BBH', 'BBR', 'BHH', 'BRR', 'BHR', 'BHN'])
    basketCounter=0
  
    for line in basketsLines.split("\n"):
        basket = [] 
        if not line:
            break;

        lineArray = line.split(",")
        
        basket.append(lineArray[3])     
        basket.append(lineArray[5])     
        basket.append(lineArray[7])    
           
        basketTotalGrade = CalculateBasketTotalGrade(basket,allTransactions)      
        
        basketsWithGradesDf.at[basketCounter, 'BasketNumber'] = lineArray[0]
        basketsWithGradesDf.at[basketCounter, 'Index'] = lineArray[1]
        basketsWithGradesDf.at[basketCounter, 'TotalBasketScore_80'] = float(lineArray[2])
        basketsWithGradesDf.at[basketCounter, 'TotalBasketScore_20'] = basketTotalGrade[0]
        basketsWithGradesDf.at[basketCounter, 'Item1'] = lineArray[3]
        basketsWithGradesDf.at[basketCounter, 'Item1Desc'] = lineArray[4]
        basketsWithGradesDf.at[basketCounter, 'Item2'] = lineArray[5]
        basketsWithGradesDf.at[basketCounter, 'Item2Desc'] = lineArray[6]
        basketsWithGradesDf.at[basketCounter, 'Item3'] = lineArray[7]
        basketsWithGradesDf.at[basketCounter, 'Item3Desc'] = lineArray[8]
        basketsWithGradesDf.at[basketCounter, 'item3Occurences'] = lineArray[9]
        basketsWithGradesDf.at[basketCounter, 'item3Dist'] = lineArray[10]

        for key in basketTotalGrade[1]:
            basketsWithGradesDf.at[basketCounter, key] = basketTotalGrade[1][key]

        endTime = time.time()
        gradesPerBasket["basket"] = basket
        gradesPerBasket["grade"] = basketTotalGrade[0]

        basketCounter = basketCounter + 1
        if (basketCounter % 10 ==0):
             gradesPerBasket.to_csv("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\ScoringBasketBy20.csv")
             excelFileName = "C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\ScoringBaskets_" 
             excelFileName += str(numberOfTransactions)
             excelFileName += "Trxs.xlsx"
             basketsWithGradesDf.to_excel(excelFileName)  
                
    allEndTime = time.time()    
    gradesPerBasket.to_csv("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\ScoringBasketBy20.csv")
    excelFileName = "C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\ScoringBaskets_" 
    excelFileName += str(numberOfTransactions)
    excelFileName += "Trxs.xlsx"
    basketsWithGradesDf.to_excel(excelFileName)  
    print("total time for all:", allEndTime - allStartTime)
    print("total time for all:", allEndTime - allStartTime, file=fileForPrint)



model = Word2Vec.load("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Model\\wfm_80.model")

#transactionsFile = open("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\Items_80.txt", "r") 
transactionsFile = open("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\items_20.csv", "r") 
#transactionsFile = open("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\Items80_9Percent_NoSingleItemBasket.txt", "r") 
transactions = transactionsFile.read() 

# clusters =  pd.read_csv("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\clustersDataFrame.csv")
# clusters =  pd.read_excel("C:\\Dev\\Innovation\\customerSegmentation\\Data\\Items\\clustersDataFrame.xlsx")
# clustersSorted = clusters.sort_values('TotalOccurences', ascending=False)
# mostconsumedItems = clustersSorted["item1Id"]


allTransactions = []
numberOfTransactionsToUse = 2000000
count = 0
for transactionLine in transactions.split("\n")[:numberOfTransactionsToUse]: 
    transactionsArray = [] 
    count = count + 1      
    for product in transactionLine.split(","): 
        word = product.replace("'",'').replace(" ",'').replace('"','')
        #if (word not in temp):
        transactionsArray.append(word)         

    if (len(transactionsArray) > 1):
        allTransactions.append(transactionsArray) 

HRT = 0.8
RT = 0.65
HRTFactor = 0.75
RTFactor= 0.375

numberOfTransactions = len(allTransactions)
print ("number of transactions:",numberOfTransactions)
print ("number of transactions:",numberOfTransactions, file=fileForPrint)

i1 = 0

# basketsByComplementary
ScoringBasketBy20()


# # seed the pseudorandom number generator
# from random import seed
# from random import random

# def CreateTenPercentOfItems_80Randomly(): 
#     seed(1) # seed random number generator
#     fileForPrint80 = open('Items80_9Percent_NoSingleItemBasket.txt', 'w') 
#     print ('started CreateTenPercentOfItems_80Randomly')
#     for transactionLine in transactions.split("\n"): 
#         rand = random()
#         # print(rand)

#         splitted = transactionLine.split(",")        
#         if ((len(splitted) > 1 ) and (rand < 0.09)):
#             print(transactionLine, file = fileForPrint80)

#     print('done')

# CreateTenPercentOfItems_80Randomly()


