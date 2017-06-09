# -*- coding: utf-8 -*-
"""
Created on Wed May  3 16:22:56 2017

@author: CELIA
"""

import reader as read
import procesador as process
import images as im


#%% Load  and filter the data

DY = read.readJsonData("Json_DY.json")
Wjets = read.readJsonData("Json_Wjets.json")
TTjets = read.readJsonData("Json_TTjets.json")
signal = read.readJsonData("Json_signal.json")

# Generate histograms before filter

im.generateAllhistograms(DY, DirName = 'DY Before Filter', origen = 'DY')
im.generateAllhistograms(TTjets, DirName = 'TTjets Before Filter', origen = 'TTjets')
im.generateAllhistograms(Wjets, DirName = 'Wjets Before Filter', origen = 'Wjets')
im.generateAllhistograms(signal, DirName = 'Signal Before Filter', origen = 'Signal')

# Filter the jets, muons and electrons

process.leptonFilter(DY, 'muon', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.leptonFilter(DY, 'electron', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.jetFilter(DY, minpt =30, maxpt = False, maxAbsEta = 2.4, jetNumber=False, tightIDFilter = True)

process.leptonFilter(TTjets, 'muon', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.leptonFilter(TTjets, 'electron', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.jetFilter(TTjets, minpt =30, maxpt = False, maxAbsEta = 2.4, jetNumber=False, tightIDFilter = True)

process.leptonFilter(Wjets, 'muon', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.leptonFilter(Wjets, 'electron', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.jetFilter(Wjets, minpt =30, maxpt = False, maxAbsEta = 2.4, jetNumber=False, tightIDFilter = True)

process.leptonFilter(signal, 'muon', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.leptonFilter(signal, 'electron', minPt = 20, maxPt = False, minEta = False, maxEta = False, tightIDFilter = True, tightIsoFilter = True)
process.jetFilter(signal, minpt =30, maxpt = False, maxAbsEta = 2.4, jetNumber=False, tightIDFilter = True)

# Histograms after lepton and jet filter

im.generateAllhistograms(DY, DirName = 'DY After Lepton and Jet Filter', origen = 'DY')
im.generateAllhistograms(TTjets, DirName = 'TTjets After Lepton and Jet Filter', origen = 'TTjets')
im.generateAllhistograms(Wjets, DirName = 'Wjets After Lepton and Jet Filter', origen = 'Wjets')
im.generateAllhistograms(signal, DirName = 'Signal After Lepton and Jet Filter', origen = 'Signal')

# Select the events with one lepton in final state

process.leptonNumberFilter(DY, electronNumber = False, muonNumber = False, leptonNumber = 1)
process.leptonNumberFilter(TTjets, electronNumber = False, muonNumber = False, leptonNumber = 1)
process.leptonNumberFilter(Wjets, electronNumber = False, muonNumber = False, leptonNumber = 1)
process.leptonNumberFilter(signal, electronNumber = False, muonNumber = False, leptonNumber = 1)

# Histograms after event filter

im.generateAllhistograms(DY, DirName = 'DY After Event Filter', origen = 'DY')
im.generateAllhistograms(TTjets, DirName = 'TTjets After Event Filter', origen = 'TTjets')
im.generateAllhistograms(Wjets, DirName = 'Wjets After Event Filter', origen = 'Wjets')
im.generateAllhistograms(signal, DirName = 'Signal After Event Filter', origen = 'Signal')

#%% Training files

import training as training
import random as random

signal_Class = training.selectClass_KnownClass(signal, ClassName = 'Signal', ClassNumber = '0')
DY_Class = training.selectClass_KnownClass(DY, ClassName = 'DY', ClassNumber = '1')
Wjets_Class = training.selectClass_KnownClass(Wjets, ClassName = 'Wjets', ClassNumber = '1')
TTjets_Class = training.selectClass_KnownClass(TTjets, ClassName = 'TTjets', ClassNumber = '1')

# 5000 events from each class are taken to the test set

test_signal_Class = []
test_DY_Class = []
test_Wjets_Class = []
test_TTjets_Class = []

for i in range(0,1666):
    test_DY_Class.append(DY_Class.pop())
    test_Wjets_Class.append(Wjets_Class.pop())
    test_TTjets_Class.append(TTjets_Class.pop())
test_DY_Class.append(DY_Class.pop()) #extra
test_Wjets_Class.append(Wjets_Class.pop()) #extra
    
for i in range(0,5000):
    test_signal_Class.append(signal_Class.pop())
    
test_Class = test_DY_Class +  test_Wjets_Class + test_TTjets_Class + test_signal_Class
random.shuffle(test_Class)
    
# 2500 events from each class are taken to the val set

val_signal_Class = []
val_DY_Class = []
val_Wjets_Class = []
val_TTjets_Class = []

for i in range(0,1000):
    val_DY_Class.append(DY_Class.pop())
    val_Wjets_Class.append(Wjets_Class.pop())
    val_TTjets_Class.append(TTjets_Class.pop())
    
for i in range(0,3000):
    val_signal_Class.append(signal_Class.pop())

val_Class = val_DY_Class +  val_Wjets_Class + val_TTjets_Class + val_signal_Class
random.shuffle(val_Class)

# The remaining events belong to the train set

#TTjets are cloned to have a balanced sample
#Wjets_newClass = training.setNumbers(Wjets_Class, 32000)
#DY_newClass = training.setNumbers(DY_Class, 32000)
signal_newClass = training.setNumbers(signal_Class, 95000)

train_Class = DY_Class + Wjets_Class + TTjets_Class + signal_newClass
random.shuffle(train_Class)

# Delete the data stored in test.txt train.txt and val.txt
test=open('Training Files/test.txt','w')
test.close()
val=open('Training Files/val.txt','w')
val.close()
train=open('Training Files/train.txt','w')
train.close() 

# Write in text training files

for n in range(0, len(test_Class)):
    training.writeTest(test_Class[n])
for n in range(0, len(val_Class)):
    training.writeVal(val_Class[n])
for n in range(0, len(train_Class)):
    training.writeTrain(train_Class[n])
    
# Get the information of the training set

import information as info

info.getTrainingInfo(classnumber = 2)

#%% Image Creation

# Draw the events

import images as im

im.generateAllEvents(DY, 'DY', 'json')

im.generateAllEvents(TTjets, 'TTjets', 'json')

im.generateAllEvents(Wjets, 'Wjets', 'json')

im.generateAllEvents(signal, 'Signal', 'json')
    
#%%  Get the results

import resultados as result
import os
import matplotlib.pyplot as plt

names = ['results_class1.txt', 'results_class0.txt']# Select the names of the files with the results

CM, normalizedCM =result.confusionMatrix(names) # Acces to the data and create a truth matrix in truth_matrix.txt

class_names = [r"$t\bar t$", r'$\mathit{Background}$']

if not os.path.exists('Results/Truth Matrix/tt bar detection'): os.makedirs('Results/Truth Matrix/tt bar detection')
Dir = 'Results/Truth Matrix/tt bar detection/'

result.plotConfusionMatrix(CM, classes = class_names,
                          normalize=False,
                          title=' ',
                          cmap=plt.cm.Reds)
plt.savefig(Dir+'Non-Normalized Confusion Matrix.png', dpi = 600)

result.plotConfusionMatrix(normalizedCM, classes=class_names, normalize=True,
                      title=' ', cmap=plt.cm.Reds)
plt.savefig(Dir+'Normalized Confusion Matrix.png', dpi = 600)

result.get_accuracy_loss('train.log', 1, 100)
    
#%% Get the ROC

import resultados as result

ttprime_filePath = 'ROC/Probabilities/tt prime/dict.json'
ttbar_filePath = 'ROC/Probabilities/tt bar/dict.json'

ttbar_Dic = result.readDict(ttbar_filePath)
ttprime_Dic = result.readDict(ttprime_filePath)

result.createROC_ttbar_divided(ttbar_Dic)
result.createROC_ttprime_divided(ttprime_Dic)

            
