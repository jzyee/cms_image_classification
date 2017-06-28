#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 10:57:03 2017

@author: celiafernandezmadrazo
"""

import training as training
import reader as read
import procesador as process
import images as im
import random as random

#%% Read and filter the data

data = read.readJsonData("Json_data.json")

process.leptonFilter(data, 'muon', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.leptonFilter(data, 'electron', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.jetFilter(data, minpt =30, maxpt = False, maxAbsEta = 2.4, jetNumber=False, tightIDFilter = True)

process.leptonNumberFilter(data, electronNumber = False, muonNumber = False, leptonNumber = 1)

print('The data have been filtered')

#%% Create the test file

data_Class = training.selectClass_KnownClass(data, ClassName = 'data', ClassNumber = '0')

print('The data list has been created')

random.shuffle(data_Class)

test=open('Training Files/Data/test.txt','w')
test.close()

for n in range(0, len(data_Class)):
    training.writeTest(data_Class[n])
    
print('The test file has been created')

    
import information as info
info.getTrainingInfo(classnumber = 1)

#%% Create the images

im.generateAllEvents(data, 'data', 'json')

print('The images have been created')

#%% Results

import resultados as result

# Samples + data histogram

ttprime_filePath = 'ROC/Probabilities/tt prime/dict_divided.json'
dataprime_filePath = 'ROC/Probabilities/tt prime/dict_data.json'

dataprime_Dic = result.readDict(dataprime_filePath)
ttprime_Dic = result.readDict(ttprime_filePath)

result.createROC_ttprimewithdata(ttprime_Dic, dataprime_Dic, normedVar = False)

# Samples + data histogram

ttbar_filePath = 'ROC/Probabilities/tt bar/dict_divided.json'
databar_filePath = 'ROC/Probabilities/tt bar/dict.json'

ttbar_Dic = result.readDict(ttbar_filePath)
databar_Dic = result.readDict(databar_filePath)

result.createROC_ttbarwithdata(ttbar_Dic, databar_Dic, normedVar = False)
