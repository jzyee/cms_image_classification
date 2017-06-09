# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 10:14:44 2017

@author: CELIA
"""

import numpy as np
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Ellipse, Rectangle
import os


def generateAllhistograms(Data, DirName, origen):
    
    # Call the other histograms functions and generate all histograms
    
    particleandjet_Histograms(Data, DirName, 'jet', origen)
    particleandjet_Histograms(Data, DirName, 'muon', origen)
    particleandjet_Histograms(Data, DirName, 'electron', origen) 
    generalMagnitude_Histogram(Data, 'met', DirName, origen)
    
    print(DirName + ' histograms created')
    
    
def generateAllEvents(Data, DataName, fileType):
    
    # Draw the events
    Data = Data
    
    Events = Data['Event']
    
    EventNames = list(Events.keys()) # list of event names (numbers)
    
    # Loop over the events
    for EventNumber in EventNames:
        
        status = [int(i*len(EventNames)/100) for i in range(0,100)]
        n = EventNames.index(EventNumber)
        if n in status:
            print (str(n)+" out of "+ str(len(EventNames)) + " completed")
        
        Event = Events[EventNumber]

        if fileType == 'json':
            drawEventJson(Event, imageName = DataName+'_event_'+EventNumber+'.jpg', Class = DataName)
        elif fileType == 'csv':
            drawEventCsv(Event, imageName = DataName+'_event_'+EventNumber+'.jpg')
            
    print('All '+DataName+' events have been created')
    
def drawEventCsv(Event, imageName):
    
    
    
    # Create the empty figure
    plt.ioff()
    fig = plt.figure(frameon=False)
    fig.set_size_inches(4,4)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.axis([-3,3,-math.pi,math.pi])
    ax.set_axis_off()
    fig.add_axes(ax)

            
    # Draw the muons
    if 'muon' in Event:
        # Loop over the electrons
        muonSet = list(Event['muon'].keys())
        for muonNumber in muonSet:
            muon = Event['muon'][muonNumber] # Get the electron
            Energy = muon['Energy']
            eta = muon['eta']
            phi = muon['phi']

            scaleEnergy = math.log(Energy,11/10)
            phiAxis = np.array([scaleEnergy*2*math.pi/224]) # Ellypse axis
            etaAxis = np.array([scaleEnergy*6/224])
            
            center = np.array([eta,phi])
            Object = Ellipse(xy = center, width=etaAxis, height=phiAxis, angle=0.0, facecolor = 'none', edgecolor= 'g', lw = 4)
            ax.add_artist(Object)
    
    # Image name
        #'event_numEvent.jpg'
    if not os.path.exists('CreatedImages/Muon Images'): os.makedirs('ImageInfo/Muon Images')
    image_dir = 'CreatedImages/Muon Images/'
    fig.savefig(image_dir+imageName, dpi=56)
    plt.close(fig) 


def drawEventJson(Event, imageName, Class):
    
    # Create the empty figure
    plt.ioff()
    fig = plt.figure(frameon=False)
    fig.set_size_inches(4,4)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.axis([-3,3,-math.pi,math.pi])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # Draw the electrons
    if 'electron' in Event:
        # Loop over the electrons
        electronSet = list(Event['electron'].keys())
        for electronNumber in electronSet:
            electron = Event['electron'][electronNumber] # Get the electron
            pt = electron['pt']
            eta = electron['eta']
            phi = electron['phi']

            scalePt = math.log(pt,11/10)
            phiAxis = np.array([scalePt*2*math.pi/224]) # Ellypse axis
            etaAxis = np.array([scalePt*6/224])
            
            center = np.array([eta,phi])
            Object = Ellipse(xy = center, width=etaAxis, height=phiAxis, angle=0.0, facecolor = 'none', edgecolor= 'b', lw = 4)
            ax.add_artist(Object)
            
    # Draw the muons
    if 'muon' in Event:
        # Loop over the electrons
        muonSet = list(Event['muon'].keys())
        for muonNumber in muonSet:
            muon = Event['muon'][muonNumber] # Get the electron
            pt = muon['pt']
            eta = muon['eta']
            phi = muon['phi']

            scalePt = math.log(pt,11/10)
            phiAxis = np.array([scalePt*2*math.pi/224]) # Ellypse axis
            etaAxis = np.array([scalePt*6/224])
            
            center = np.array([eta,phi])
            Object = Ellipse(xy = center, width=etaAxis, height=phiAxis, angle=0.0, facecolor = 'none', edgecolor= 'g', lw = 4)
            ax.add_artist(Object)
            
    # Draw the jets
    if 'jet' in Event:
        # Loop over the electrons
        jetSet = list(Event['jet'].keys())
        for jetNumber in jetSet:
            jet = Event['jet'][jetNumber] # Get the electron
            pt = jet['pt']
            eta = jet['eta']
            phi = jet['phi']
            CSV = jet['CSV']

            scalePt = math.log(pt,11/10)
            phiAxis = np.array([scalePt*2*math.pi/224]) # Ellypse axis
            etaAxis = np.array([scalePt*6/224])
            
            # Define the color of the jet object
#            if CSV > 2 or CSV == 2:
#                colorScale = 0
#            elif CSV<0:
#                colorScale = 225
#            else:
#                colorScale = 200-100*CSV
            if CSV>0.679: # medium working point
                colorScale = 0 # b-tag
            else: 
                colorScale = 125 # no b-tag
                
            colorRGB = colorScale/255
            
            center = np.array([eta,phi])
            Object = Ellipse(xy = center, width=etaAxis, height=phiAxis, angle=0.0, facecolor = 'none', edgecolor= (1, colorRGB, colorRGB), lw = 4)
            ax.add_artist(Object)
            
    # Draw the met
    if 'met' in Event:
        met = Event['met']
        scaleMet = math.log(met,11/10)
        met_phi = Event['met_phi']
        phiAxis = np.array([scaleMet*2*math.pi/224]) # Ellypse axis
        etaAxis = np.array([scaleMet*6/224])
        center = np.array([0,met_phi])
        Object = Ellipse(xy = center, width=etaAxis, height=phiAxis, angle=0.0, facecolor = 'none', edgecolor= 'k', lw = 4)
        #Object = Rectangle(xy = np.array([3*9/10, 9/10*math.pi]), width = 0.08*3, height = 0.08*math.pi, angle = 0.0, facecolor = color, edgecolor = color)
        ax.add_artist(Object)
    
    # Image name
        #'event_numEvent.jpg'
    if not os.path.exists('CreatedImages/'+Class+ ' Images'): os.makedirs('CreatedImages/'+Class+ ' Images')
    image_dir = 'CreatedImages/'+Class+ ' Images/'
    fig.savefig(image_dir+imageName, dpi=56)
    plt.close(fig) 
    


def particleandjet_Histograms(Data, DirName, elementName, origen):
    
    if not os.path.exists('Histograms/'+DirName): os.makedirs('Histograms/'+DirName) 
    
    #Access to the events
    Events = Data['Event']
    EventNames = list(Events.keys()) # list of event names (numbers)]
    
    # Inicialize variables:
    ptSet = []
    etaSet = []
    phiSet = []
    pxSet = []
    pySet = []
    pzSet = []
    CSVSet = []
    
    for EventNumber in EventNames:
        
        if elementName in Events[EventNumber]:
            
            particleSet = Events[EventNumber][elementName]
            particles = list(particleSet.keys())
            for particle in particles:
                
                if elementName != 'jet':
                    
                    pt = particleSet[particle]['pt']
                    eta = particleSet[particle]['eta']
                    phi = particleSet[particle]['phi']
                    px = particleSet[particle]['px']
                    py = particleSet[particle]['py']
                    pz = particleSet[particle]['pz']
    
                    ptSet.append(pt)
                    etaSet.append(eta)
                    phiSet.append(phi)
                    pxSet.append(px)
                    pySet.append(py)
                    pzSet.append(pz)
                    
                else:
                    
                    pt = particleSet[particle]['pt']
                    eta = particleSet[particle]['eta']
                    phi = particleSet[particle]['phi']
                    CSV = particleSet[particle]['CSV']
    
                    ptSet.append(pt)
                    etaSet.append(eta)
                    phiSet.append(phi)
                    CSVSet.append(CSV)
                
    variable = {'pt': ptSet, 'eta':etaSet, 'phi':phiSet, 'px':pxSet, 'py':pySet, 'pz':pzSet, 'CSV': CSVSet}
    #bins = {'pt': ptSet, 'eta':etaSet, 'phi':phiSet, 'px':pxSet, 'py':pySet, 'pz':pzSet}
    
    # Generate the histograms
    
    
    if elementName == 'jet':
        jetList = ['pt', 'eta', 'phi', 'CSV']
        c = 'r'
        for magnitude in jetList:

            plt.ioff()
            plt.clf()
            
            if magnitude == 'eta':
                plt.hist(variable[magnitude], bins = np.linspace(-5,5,50), log = True, color = c, label = origen)
                #plt.xscale('symlog')
                plt.yscale('log', nonposy='clip')
            elif magnitude == 'phi':
                plt.hist(variable[magnitude], bins = np.linspace(-math.pi,math.pi,50), log = True, color = c, label = origen)
                plt.yscale('log', nonposy='clip')
            elif magnitude == 'CSV':
                maxValue = max(variable[magnitude])
                plt.hist(variable[magnitude], bins = np.linspace(-100,maxValue,100), log = True, color = c, label = origen)
                plt.yscale('log', nonposy='clip')
            else:
                maxValue = max(variable[magnitude])
                maxPoint = math.log(maxValue,10)
                
                plt.hist(variable[magnitude], bins = np.logspace(0, maxPoint, 100), color = c, log = True, label = origen)
                plt.semilogx()
            
            plt.legend(loc='upper right')
            plt.title(elementName+' '+magnitude+' '+DirName)
            plt.xlabel(elementName +' '+magnitude)
            plt.ylabel(elementName + 's')
            plt.savefig('Histograms/'+DirName+'/'+elementName +'_'+magnitude+'_'+'Histogram.png')
            plt.close()
            
    else:
        particleList = ['pt', 'eta', 'phi', 'px', 'py', 'pz']
        
        if elementName == 'electron':
            c = 'b'
        elif elementName == 'muon':
            c = 'g'

        for magnitude in particleList:
            
            plt.ioff()
            plt.clf()
            
            if magnitude == 'eta':
                plt.hist(variable[magnitude], bins = np.linspace(-5,5,50), log = True, color = c, label=origen)
                plt.yscale('log', nonposy='clip')
                #plt.xscale('symlog')
            elif magnitude == 'phi':
                plt.hist(variable[magnitude], bins = np.linspace(-math.pi,math.pi,50), log = True, color = c, label = origen)
                plt.yscale('log', nonposy='clip')
            else:
                maxValue = max(variable[magnitude])
                maxPoint = math.log(maxValue,10)
                
                plt.hist(variable[magnitude], bins = np.logspace(0, maxPoint, 100), color = c, log = True, label=origen)
                plt.semilogx()
            
            plt.legend(loc='upper right')
            plt.xlabel(elementName +' '+magnitude)
            plt.ylabel(elementName + 's')
            plt.savefig('Histograms/'+DirName+'/'+elementName +'_'+magnitude+'_'+DirName+' '+'Histogram.png')
            plt.close()


def generalMagnitude_Histogram(Data, magnitude, DirName, origen):
    
    if not os.path.exists('Histograms/'+DirName): os.makedirs('Histograms/'+DirName) 
    
    #Access to the events
    Events = Data['Event']
    EventNames = list(Events.keys()) # list of event names (numbers)]
    
    magnitudeSet = [] # Empty variable

    for EventNumber in EventNames:
        value = Events[EventNumber][magnitude]
        magnitudeSet.append(value)
        
    plt.ioff()
    plt.clf()
    maxValue = max(magnitudeSet)
    maxPoint = math.log(maxValue,10)
    plt.hist(magnitudeSet, bins = np.logspace(0, maxPoint, 100), color = 'b', log = True, label=origen)
    plt.semilogx()
    if magnitude == 'mass':
        units = '(GeV/$c^2$)'
    elif magnitude == 'met':
        units = '(GeV)'
    plt.legend(loc='upper right')
    plt.xlabel(magnitude+' '+units)
    plt.ylabel('Events')
    plt.savefig('Histograms/'+DirName+'/'+magnitude+'_'+origen+'_'+'Histogram.png')
    plt.close()

    