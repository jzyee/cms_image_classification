# -*- coding: utf-8 -*-
"""
Created on Tue May  2 12:16:07 2017

@author: CELIA
"""

import json
import time

    
def readCsvData(fileName):
    
    Data = {'Event':{}} # Create the empty variable data
    Events = {} # Empty variable events
    
    # Open the file
        # The file must be located in folder 'Data'
    dataFile = open('Data/'+fileName,'r')
    
    # Read the heading
        # Create a list with the parameters of the particles of the csv file
    parameters = dataFile.readline()   
    parameters = parameters.split(',')
    parameters[-1]=parameters[-1][:len(parameters[-1])-1] # Remove the '\n' term


    # Loop over the lines of the file and storing the particles

    particles = dataFile.readlines()
    
    currentEvent = 'none'
    
    for particle in particles:
        
        #t0 = time.clock()
        particleList = particle.split(',')
        particleList.pop(-1)
        EventNumber = particleList[0]
        MuonNumber = particleList[1]
        # Construc the muon element (default)
        Muon = {}
        for n in range(2, len(parameters)):
            Muon[parameters[n]] = float(particleList[n]) # Assign values
        
        # Introduce the muon in data
            # If the event is equal to the last one it adds the particles to it
            # If the event does not exist it creates it
        
        if EventNumber == currentEvent:
            
            Events[EventNumber]['muon'][MuonNumber] = Muon
        
        else:
            Events[EventNumber] = {} # Create the event
            Events[EventNumber]['muon'] = {} # Create the set of muons
            Events[EventNumber]['muon'][MuonNumber] = Muon # Add the muon
            currentEvent = EventNumber
            
        
        #t1 = time.clock()
        #executionTime = t1-t0
        status = [int(i*len(particles)/100) for i in range(0,100)]
        
        if particles.index(particle) in status:
            print (str(particles.index(particle) )+" out of "+ str(len(particles)) + " completed")
        
    Data['Event'] = Events
    dataFile.close() # close the file
    return Data
    
def readJsonData(fileName):
    
    with open('Data/'+fileName) as dataFile:    
        Data = json.load(dataFile) # Load the data (the format is included)

    return Data
    
    
def completeData(Data):
    
    # This function is designed to complete the data stored in csv files
        # The information added to the data variable simplifies the operations
        # that are carried out by other functions
        
    Events = Data['Event']
    EventNames = list(Events.keys())
    
    # Loop over the events
    for EventNumber in EventNames:
        
        muons = Events[EventNumber]['muon']
        muonSet = list(muons.keys())
        nummu = len(muonSet) # Number of muons
        Events[EventNumber]['nummu'] = nummu
        
        # Extra info
        Events[EventNumber]['numel'] = 0 # Default
        Events[EventNumber]['njet'] = 0 # Default
        