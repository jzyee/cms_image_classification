# -*- coding: utf-8 -*-
"""
Created on Wed May  3 18:13:16 2017

@author: CELIA
"""

import random as random
import numpy as np
import os


def selectClass_InvariantMass(Data, setNumbers, origen):
    
    # It creates a new list with image name and its decay class 
        # If setNumbers is True it balances the sample.
        ## MUON EXAMPLE ONLY
    
    numClass = 5
    Class = []
    Events = Data['Event']
    if setNumbers:

        #Receives the vector data and the number of classes
        counter = np.zeros(numClass)
        EventNames = list(Events.keys())
        for EventNumber in EventNames:
            c = int(Events[EventNumber]['class'])
            counter[c]+=1
    
        factor= np.amax(counter)/counter
        
        for n in range(0,len(factor)):
            factor[n] = int(factor[n])
            
        for EventNumber in iter(Events):
            c = int(Events[EventNumber]['class'])
            for times in range(0,int(factor[c])):
                ImageName = origen+'event_'+EventNumber+'.jpg'
                Class.append([ImageName, Events[EventNumber]['class']])
        
    else:
        
        for EventNumber in iter(Events):
            ImageName = origen+'event_'+EventNumber+'.jpg'
            Class.append([ImageName, Events[EventNumber]['class']])
            
    random.shuffle(Class)
    return Class

def selectClass_KnownClass(Data, ClassName, ClassNumber):
    
    # It adds a label with the class number to the variable data and creates a new variable with the name of the image and its class
    
    # Initiallize the variable
    Class = []
    
    # Access the event
    Events = Data['Event']

    # Loop over the events
    for EventNumber in iter(Events):
        
        Events[EventNumber]['class'] = ClassNumber
        ImageName = ClassName+'_event_'+EventNumber+'.jpg'
        Class.append([ImageName, ClassNumber])
        
    return Class
    
def setNumbers(Class, num):
    
    # This function clones the elements of a list to have a balanced sample
    
    newClass = Class[:] # creates a new copy of the list
    
    while len(newClass)<num:
        
        for element in Class:
            
            if len(newClass) < num:
                
                newClass.append(element)
    
    return newClass



def writeTrain(Class):
    
    # Write the train.txt file
    
    Dir = 'Training Files/'
    My_text=open(Dir+'train.txt','a')
    My_text.write(Class[0]+' '+Class[1]+'\n')
    My_text.close()        


def writeVal(Class):
    
    # Write the val.txt file
    
    Dir = 'Training Files/'
    My_text=open(Dir+'val.txt','a')
    My_text.write(Class[0]+' '+Class[1]+'\n')
    My_text.close()  

def writeTest(Class):
    
    # Write the test.txt file
    
    Dir = 'Training Files/Data/'
    My_text=open(Dir+'test.txt','a')
    My_text.write(Class[0]+' '+Class[1]+'\n')
    My_text.close() 