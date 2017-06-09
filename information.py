# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:21:21 2017

@author: CELIA
"""
import numpy as np
import os

def getCsvImageInfo(Data, origen):
    
    if not os.path.exists('ImageInfo/CsvData'): os.makedirs('ImageInfo/CsvData') 
    data_file = open('ImageInfo/CsvData/Info_'+origen+'_data'+'.txt', 'w')
    
    data_file.write('IMAGE INFORMATION '+ '\n') # Write the title
    data_file.write('\n')
    data_file.write('Image name'+'\t'+'eta'+'\t'+'phi'+'\t'+'Energy'+'\t'+'Invariant Mass'+'\t'+'Class '+'\n') # Write the heading
    
    Events = Data['Event'] # Access the data
    EventNames = list(Events.keys()) 
    EventNames.sort()

    # Loop over the events 
    for EventNumber in EventNames:
        
        imageName = origen+'event_'+EventNumber+ '.jpg' # Get the name of the image
        Mass = str(Events[EventNumber]['mass']) # Get the invariant mass
        Class = str(Events[EventNumber]['class']) # Get the class of the event
        
        # Type of particle is set at 'muon' by default
            # Csv files only have muons
        muonSet = Events[EventNumber]['muon']
        # loop over the particles
        for muon in iter(muonSet):
            # Write the particle data
            data_file.write(imageName +'\t' + str(muonSet[muon]['eta'])+'\t' + str(muonSet[muon]['phi'])+'\t'+str(muonSet[muon]['Energy'])+'\t'+Mass+'\t'+ Class + '\n')
    
    data_file.close() # Close the file

def getJsonImageInfo(Data):
    
    # Descripción de la función
    
    Events = Data['Evento']
    EventNames = list(Events.keys())
    data_file = open('ImageInfo/data_info.txt', 'w')
    data_file.write('IMAGE INFORMATION '+ '\n') # Write the title
    data_file.write('\n')




def getTrainingInfo(classnumber):
    
    #TRAIN INFORMATION
    train = open('Training Files/train.txt','r')
    train_info=np.zeros(classnumber)
    
    lines = train.readlines()
    for line in lines:
        list_line = line.split()
        train_info[int(list_line[1])] +=1
    train.close()
    
    #VAL INFORMATION
    val = open('Training Files/val.txt','r')
    val_info=np.zeros(classnumber)
    
    lines = val.readlines()
    for line in lines:
        list_line = line.split()
        val_info[int(list_line[1])] +=1
    val.close()
    
    #TEST INFORMATION
    test = open('Training Files/test.txt','r')
    test_info=np.zeros(classnumber)
    
    lines = test.readlines()
    for line in lines:
        list_line = line.split()
        test_info[int(list_line[1])] +=1
    test.close()
    
    #Write information in a file
    info = open('Training Info/info.txt','w')
    info.write('TRIAL INFORMATION: '+str(classnumber)+' classes'+'\n')
    info.write('\n')
    info.write('Number of samples: '+str(sum([np.sum(train_info), np.sum(val_info), np.sum(test_info)]))+ '\n')
    info.write('\n')
    
    info.write('train: '+'\n')
    for x in range(0,len(train_info)):
        info.write('Class '+str(x)+': '+str(train_info[x])+'\t'+ str(train_info[x]/np.sum(train_info))+'%'+'\n')
    info.write('Total: '+str(np.sum(train_info))+'\n')
    info.write('\n')
    
    info.write('val: '+'\n')
    for x in range(0,len(val_info)):
        info.write('Class '+str(x)+': '+str(val_info[x])+'\t'+ str(val_info[x]/np.sum(val_info))+'%'+'\n')
    info.write('Total: '+str(np.sum(val_info))+'\n')
    info.write('\n')
    
    info.write('test: '+'\n')
    for x in range(0,len(test_info)):
        info.write('Class '+str(x)+': '+str(test_info[x])+'\t'+ str(test_info[x]/np.sum(test_info))+'%'+'\n')
    info.write('Total: '+str(np.sum(test_info))+'\n')
    info.write('\n')
    
    info.close()
    
def return_class_number(Data, classNumber):
    Run = Data['Run']
    i = 0 #counter
    for run_data in Run:
        if run_data['Class']==classNumber:
            i +=1
    return i
    