
import pandas as pd
import gensim 
from gensim.models import Word2Vec 





NUM_CLUSTERS=300

sample = open("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Items\\Items_80.txt", "r") 
s = sample.read() 

data = []

for line in s.split("\n"): 
    temp = [] 
      

    

    for j in line.split(","): 
        temp.append(j.replace("'",'').replace(" ",'')) 
  
    data.append(temp) 
  

model = gensim.models.Word2Vec(data, min_count = 1,  
                              size = 100, window = 10) 


model.save("C:\\Dev\\Innovation\\CustomerSegmentation\\Data\\Model\\wfm_80.model")

