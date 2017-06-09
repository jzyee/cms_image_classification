# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 23:18:11 2017

@author: Celia Fernández Madrazo
"""
import reader as read
import procesador as process
import os

#%% Read and complete the data

# Read the data
mytreeData = read.readCsvData('Photo_data_filtered_mytree.csv')
mytree2011Data = read.readCsvData('Photo_data_filtered_mytree2011.csv')  

# Complete the data
read.completeData(mytreeData)
read.completeData(mytree2011Data)

#%% Filter the data 

# Events with 2 particles
process.leptonNumberFilter(mytreeData, electronNumber = False, muonNumber= 2, leptonNumber = False) 
process.leptonNumberFilter(mytree2011Data, electronNumber = False, muonNumber = 2, leptonNumber = False) 

# Particle-antiparticle pairs
process.selectionDecay(mytreeData) 
process.selectionDecay(mytree2011Data)

#%% Mass invariant and class calculations

# Compute the invariant mass of the pairs
process.invariantMassCouple(mytreeData) 
process.invariantMassCouple(mytree2011Data) 

# Choose the mass invariant class
process.decayIdentification(mytreeData) 
process.decayIdentification(mytree2011Data)


#%% Training calculations and files

import training as training

mytreeClass = training.selectClass_InvariantMass(mytreeData, setNumbers = False, origen = 'mytree') # create the list with the names of the images of mytree data and their class
mytree2011Class = training.selectClass_InvariantMass(mytree2011Data, setNumbers = True, origen = 'mytree') # create the list with the names of the images of 2011 data and their class

# Delete the data stored in test.txt train.txt and val.txt
test=open('Training Files/test.txt','w')
test.close()
val=open('Training Files/val.txt','w')
val.close()
train=open('Training Files/train.txt','w')
train.close() 

# Loop over the first half of the mytreeClass elements
for n in range(0, int(len(mytreeClass)/2)):  
    training.writeVal(mytreeClass[n]) # write the event into the val file
    
# Loop over the second half of the mytreeClass elements
for n in range(int(len(mytreeClass)/2), len(mytreeClass)):
    training.writeTest(mytreeClass[n]) # write the event into the test file
                      
                     
 # Loop over the events of 2011Class elements 
status = [int(i*len(mytree2011Class)/100) for i in range(0,100)]                  
for n in range(0, len(mytree2011Class)):
    if n in status:
        print (str(n)+" out of "+ str(len(mytree2011Class)) + "completed")
    training.writeTrain(mytree2011Class[n])


#%% Generate the histograms

import images as im

# Muon histograms
im.particleandjet_Histograms(mytreeData, DirName = 'mytree', elementName = 'muon', origen = 'tree 1')
im.particleandjet_Histograms(mytree2011Data, DirName = 'mytree2011', elementName = 'muon', origen = 'tree 2')

# Invariant mass histograms
im.generalMagnitude_Histogram(mytreeData, magnitude = 'mass', DirName = 'mytree', origen = 'tree 1')
im.generalMagnitude_Histogram(mytree2011Data, magnitude = 'mass', DirName = 'mytree2011', origen = 'tree 2')


#%% Generate the images

# mytree data events images----------------------------------------------------

Events = mytreeData['Event']

EventNames = list(Events.keys()) # list of event names (numbers)
EventNames.sort()

# Loop over the events
for EventNumber in EventNames:
    
    status = [int(i*len(EventNames)/100) for i in range(0,100)]
    n = EventNames.index(EventNumber)
    if n in status:
        print (str(n)+" out of "+ str(len(EventNames)) + " completed")
    
    Event = Events[EventNumber]
    imageName = 'mytree'+'event_'+EventNumber+'.jpg'
    im.drawEventCsv(Event, imageName)

    
# mytree2011 data events images------------------------------------------------

Events = mytree2011Data['Event']

EventNames = list(Events.keys()) # list of event names (numbers)
EventNames.sort()

# Loop over the events
for EventNumber in EventNames:
    
    status = [int(i*len(EventNames)/100) for i in range(0,100)]
    n = EventNames.index(EventNumber)
    if n in status:
        print (str(n)+" out of "+ str(len(EventNames)) + " completed")
    
    Event = Events[EventNumber]
    imageName = '2011'+'event_'+EventNumber+'.jpg'
    im.drawEventCsv(Event, imageName)

#%% Get the information about the data and training

import information as info

# Get data information
info.getCsvImageInfo(mytreeData, origen = 'mytree')
info.getCsvImageInfo(mytree2011Data, origen = '2011')

# Get training information
info.getTrainingInfo(classnumber = 5)

#%% Get the results of the training

import resultados as result
import matplotlib.pyplot as plt

names = ['results_class0.txt', 'results_class1.txt', 'results_class2.txt', 'results_class3.txt', 'results_class4.txt'] # Select the names of the files with the results

CM, normalizedCM =result.confusionMatrix(names) # Acces to the data and create a truth matrix in truth_matrix.txt

class_names = [r'$No-decay$', r'$J/\Psi$', r"$Psi'$", r'$\Upsilon$', r'$Z$']

if not os.path.exists('Results/Truth Matrix/Muon trial'): os.makedirs('Results/Truth Matrix/Muon trial')
Dir = 'Results/Truth Matrix/Muon trial/'

result.plotConfusionMatrix(CM, classes = class_names,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Reds)
plt.savefig(Dir+'Non-Normalized Confusion Matrix.png')

result.plotConfusionMatrix(normalizedCM, classes=class_names, normalize=True,
                      title='Normalized confusion matrix', cmap=plt.cm.Reds)
plt.savefig(Dir+'Normalized Confusion Matrix.png')

result.get_accuracy_loss('train.log')