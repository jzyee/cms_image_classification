# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 19:41:28 2017

@author: CELIA
"""

import random as random
import numpy as np



# %% LEPTON CHARACTERISTICS FILTERS
        
                
def leptonFilter(Data, leptonType, minPt, maxPt, minEta, maxEta, tightIDFilter, tightIsoFilter):
    
    # Function that deletes the electrons that do not fulfill the criteria given as an input
        # Criteria on min and max pt and min and max eta value
        # Inputs can be False (bool) and criteria values (float)
        # leptonType indicates if the filters should be imposed to electrons or muons
        # tightID and tightIso filters can be false or true (they do not require any numberical value)
    
    # Initial filters of pt and eta are set are turned off
    minPtFilter = False
    maxPtFilter = False
    minEtaFilter = False
    maxEtaFilter = False
    
    # If the input is different from False (bool) the filters are turned on
    if type(minPt) != bool:
        minPtFilter = True
    if type(maxPt) != bool:
        maxPtFilter = True
    if type(minEta) != bool:
        minEtaFilter = True
    if type(maxEta) != bool:
        maxEtaFilter = True
    
    # Access to the events
    Events = Data['Event']
    EventNames = list(Events.keys())
    # Loop over the events
    for EventNumber in EventNames:
        
        if leptonType in list(Events[EventNumber].keys()):
            
            leptonSet = Events[EventNumber][leptonType]
            leptons_ini = list(leptonSet.keys()) # initial leptons
            
            # Loop over the leptons of the event
            for leptonNumber in leptons_ini:
        
                # Access to variables
                pt = leptonSet[leptonNumber]['pt']
                eta = leptonSet[leptonNumber]['eta']
                tightID = leptonSet[leptonNumber]['tightID']
                tightIso = leptonSet[leptonNumber]['tightIso']
                
                if tightIDFilter and not tightID: 
                    # If the lepton is not correctly identified
                    del leptonSet[leptonNumber]
                elif tightIsoFilter and not tightIso:
                    # If the lepton is not isolated
                    del leptonSet[leptonNumber]
                elif minPtFilter and pt<minPt:
                    del leptonSet[leptonNumber]
                elif maxPtFilter and pt>maxPt:
                    del leptonSet[leptonNumber]
                elif minEtaFilter and eta<minEta:
                    del leptonSet[leptonNumber]
                elif maxEtaFilter and eta>maxEta:
                    del leptonSet[leptonNumber]
            
            # Redefine the number of leptons in the event
            leptons_fin = list(leptonSet.keys()) # Final leptons
            
            if leptonType == 'muon':
                Events[EventNumber]['nummu'] = len(leptons_fin)
            elif leptonType == 'electron':
                Events[EventNumber]['numel'] = len(leptons_fin)
            
            
def leptonNumberFilter(Data, electronNumber, muonNumber, leptonNumber):
    
    # leptonNumberFilter delete the events that do not contain the number of particles specified as an input
        # If the input is bool = False the function does not apply any filter
    
    # Initially filters are turned off
    electronFilter = False
    muonFilter = False
    leptonFilter = False
    
    # If the input is a float value instead of False (bool), the filters are turned on
    if type(electronNumber) != bool:
        electronFilter = True
    if type(muonNumber) != bool:
        muonFilter = True
    if type(leptonNumber) != bool:
        leptonFilter = True
    
    # Access the events
    Events = Data['Event']
    EventNames = list(Events.keys())
    # Loop over the events
    for EventNumber in EventNames:
        if 'electron' in list(Events[EventNumber].keys()):
            numel = len(list(Events[EventNumber]['electron'].keys())) # electron number
        else:
            numel = 0
        if 'muon' in list(Events[EventNumber].keys()):
            nummu = len(list(Events[EventNumber]['muon'].keys())) # muon number
        else:
            nummu = 0
        numlep = numel + nummu # total lepton number
        
        # If there is a restriction on one lepton number given and the number of particles does not match with it, the event is deleted.
        
        if electronFilter and electronNumber != numel:
            del Events[EventNumber]
        elif muonFilter and muonNumber != nummu:
            del Events[EventNumber]
        elif leptonFilter and leptonNumber != numlep:
            del Events[EventNumber]
    
# %% JET CHARACTERISTICS FILTERS


def jetFilter(Data, minpt, maxpt, maxAbsEta, jetNumber, tightIDFilter):
    
    # JetFilter allow us to both delete certain jets and delete certain events based on jet characteristics criteria
    
    # Initially filters are turned off  
    numberJetFilter = False
    minptFilter = False
    maxptFilter = False
    maxAbsEtaFilter = False
        
    # If the input is a float value instead of False (bool), the filters are turned on
    if type(jetNumber) != bool:
        numberJetFilter = True
    if type(minpt) != bool:
        minptFilter = True
    if type(maxpt) != bool:
        maxptFilter = True
    if type(maxAbsEta) != bool:
        maxAbsEtaFilter = True

    # Access the events
    Events = Data['Event']
    EventNames = list(Events.keys())

    # pt value jet filter:
        # All the jets with pt value out of the inverlal [minpt,maxpt] are not considered as jets
    # Loop over the events:
    for EventNumber in EventNames:

        if 'jet' in list(Events[EventNumber].keys()):
        
            jetElements = Events[EventNumber]['jet']
            jets_ini = list(jetElements.keys()) # initial jets
            
            # pt value jet filter:
                # All the jets with pt value out of the inverlal [minpt,maxpt] are not considered as jets
                # Loop over the events:
            if minptFilter or maxptFilter or maxAbsEtaFilter or tightIDFilter:
                
                for jet in jets_ini:
                    pt = jetElements[jet]['pt']
                    eta = jetElements[jet]['eta']
                    tightID = jetElements[jet]['tightID']                    

                    # Delete the jets that do not follow the criteria
                    if tightIDFilter and not tightID:
                        del jetElements[jet]
                    elif pt<minpt and minptFilter:
                        del jetElements[jet]
                    elif pt>maxpt and maxptFilter:
                        del jetElements[jet]
                    elif eta>maxAbsEta and maxAbsEtaFilter:
                        del jetElements[jet]
                    elif eta<-maxAbsEta and maxAbsEtaFilter:
                        del jetElements[jet]
    
            
            # Redefine the number of jets in the event after the selection
            jets_fin = list(jetElements.keys()) # final jets
            njet = len(jets_fin)
            Events[EventNumber]['njet'] = njet

        # Number of jets event filter:
            # All the events with a different number of jets from the jetNumber given as an input are deleted from the data
            # The number of jets only consider the jets within the range [minpt,maxpt] given as an input
        if numberJetFilter and Events[EventNumber]['njet'] != jetNumber:
            del Events[EventNumber]
            
        
#%% GENERAL EVENT CHARACTERISTICS FILTERS    

def metValueFilter(Data, minMet, maxMet):
    
    # This function deletes the events that not follow the missing transverse energy criteria
    
    minMetFilter = False
    maxMetFilter = False
    if type(minMet) != bool:
        minMetFilter = True
    if type(maxMet) != bool:
        maxMetFilter = True
    
    # Access the events
    Events = Data['Event']
    EventNames = list(Events.keys())
    # Loop over the events
    for EventNumber in EventNames:
        met = Events[EventNumber]['met'] # met value
        
        # If there is a restriction on met value and the event does not match with it, the event is deleted.
        if minMetFilter and met<minMet:
            del Events[EventNumber]

        elif maxMetFilter and met>maxMet:
            del Events[EventNumber]

#%% FUNCTIONS FOR TWO PARTICLE EVENTS (Muon example)

def invariantMassCouple(Data):
    
    # This function computes the invariant mass of a set of events with two particles
    
    # Access the events
    Events = Data['Event']
    EventNames = list(Events.keys())
    # Loop over the events
    for EventNumber in EventNames:
        
        muons = Events[EventNumber]['muon']
        muonSet = list(muons.keys())
        
        #Computes the invariant mass of the pair of particles
        pe = muons[muonSet[0]]['px']* muons[muonSet[1]]['px'] + muons[muonSet[0]]['py']* muons[muonSet[1]]['py'] + muons[muonSet[0]]['pz']* muons[muonSet[1]]['pz']
        
        eventMass = ((2*(0.1056583745)**2 + 2*(muons[muonSet[0]]['Energy']*muons[muonSet[1]]['Energy'] - pe))**(1/2))
        
        #Add the invariant mass to data variable
        Events[EventNumber]['mass'] = eventMass


def selectionDecay(Data):
    
    # This function only works with sets of events with only two particles
        # It deletes those pairs whose particles have the same charge
        # The remaining pairs are particle-antiparticle pairs
    
    # Access the events
    Events = Data['Event']
    EventNames = list(Events.keys())
    # Loop over the events
    for EventNumber in EventNames:
        
        muons = Events[EventNumber]['muon']
        
        muonSet = list(muons.keys())
        charge1 = muons[muonSet[0]]['Charge']
        charge2 = muons[muonSet[1]]['Charge']

        if charge1*charge2 == 1.0:
            del Events[EventNumber]

    

def decayIdentification(Data):
    
    # This function read the invariant mass of the events and put labels to them
        # The labels are written in a new variable 'class'
            # There are 5 criteria identification:
            # JPsi -> 1
            # Psi' -> 2
            # Upsilon -> 3
            # Z -> 4
            # None of them -> 0    
    
    mZ = 91.1876 # GeV/c2 Z Boson mass
    mUps = 9.460 # GeV/c2 Upsilon Boson mass
    mJPsi = 3.092 # GeV/c2 J/Psi boson mass
    mPsi = 3.8 # GeV/c2 Psi prime boson mass
    LZ = 15 # GeV/c2 Z Boson width
    LUps = 6 # GeV/c2 Upsilon Boson width 
    LJPsi = 0.3 # GeV/c2 J/Psi Boson width 
    LPsi = 0.3 # GeV/c2 Psi prime Boson width 
    

    # Access the events
    Events = Data['Event']
    EventNames = list(Events.keys())
    # Loop over the events
    for EventNumber in EventNames:
        Event = Events[EventNumber]
        if (Event['mass']>(mZ-LZ/2)) & (Event['mass']<(mZ+LZ/2)):
            Event['class'] = '4'
        elif (Event['mass']>(mUps-LUps/2)) & (Event['mass']<(mUps+LUps/2)):
            Event['class'] = '3'
        elif (Event['mass']>(mPsi-LPsi/2)) & (Event['mass']<(mPsi+LPsi/2)):
            Event['class'] = '2'
        elif (Event['mass']>(mJPsi-LJPsi/2)) & (Event['mass']<(mJPsi+LJPsi/2)):
            Event['class'] = '1'
        else:
            Event['class'] = '0'


    
    
    