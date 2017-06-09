# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 12:52:15 2017

@author: CELIA
"""


import json as json
import _pickle as pickle
import numpy as np
import matplotlib.pyplot as plt
import itertools
import ast


def truth_matrix(names):
    
    # It creates a text file with the truth matrix data (better version later)
        # names is a list with the names of the result text files
    
    numClass = len(names)
    results = []
    Dir = 'Results/'
    for name in names:
        my_file = open(Dir + name, 'r')
        counter = np.zeros(numClass)
        data = my_file.read()
        my_file.close()
        for s in range(0, len(data)):
            if data[s]=='[':
                counter[int(data[s+1])] +=1
        results.append(counter)
        
            
    file_results = open(Dir + 'truth_matrix.txt', 'w')
    
    file_results.write('Truth' +'\t' + '0' + '\t' +'1' + '\t' + '2'+ '\t' + '3' + '\t' + '4' + '\n') #Write the heading     

    for r in range(0, len(results)):
        file_results.write(str(r))
        for e in results[r]:
            file_results.write('\t' + str(int(e)))
        file_results.write('\n')
        
    file_results.write('\n')
    file_results.write('---------')
    file_results.write('\n')
    
    file_results.write('Truth' +'\t' + '0' + '\t' +'1' + '\t' + '2'+ '\t' + '3' + '\t' + '4' + '\n') #Write the heading   again   

    for r in range(0, len(results)):
        file_results.write(str(r))
        for e in results[r]:
            file_results.write('\t' + str(e*100/np.sum(results[r]))[:4]+'%')
        file_results.write('\n')
    
    file_results.close()

    return results  

#%% CONFUSION MATRIX

def confusionMatrix(names):
    # names is a list with the names of the result text files
    numClass = len(names)
    results = []
    Dir = 'Results/'
    for name in names:
        my_file = open(Dir + name, 'r')
        counter = np.zeros(numClass)
        data = my_file.read()
        my_file.close()
        for s in range(0, len(data)):
            if data[s]=='[':
                counter[int(data[s+1])] +=1
        results.append(counter)
        
    ### Quitar esto después: ###
    results2 = []
    results2.append(results[1])
    results2.append(results[0])
    ############################
    
    CM = np.array(results2)
    normalizedCM = CM.astype('float') / CM.sum(axis=1)[:, np.newaxis]
    return CM, normalizedCM
    
def plotConfusionMatrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.ioff()
    plt.clf()
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    if normalize:
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, "%.2f" % cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    #plt.tight_layout()
    plt.ylabel('True label', )
    plt.xlabel('Predicted label')

#%% TRAINING INFORMATION

def get_accuracy_loss(filename, resolution, epochRange):
    
    # It reads a file with information of the training and obtain the results
    
    # Access the train file
    Dir ='Results/Progress/' 
    file_input = open(Dir+filename, 'r')
    lines = file_input.readlines()
    lines.pop(-1)
    
    # Inicialize variables
    progress = []
    accuracy = []
    loss = []
    

    # Get the variable values
    for line in lines:
        if line[0] == 'T':
            parts = line.split()
            epoch = float(parts[2]) # Epoch
            completed = float(parts[4][:-1]) # Epoch percent
            accurate = float(parts[-1][0:-1]) # Accuracy
            lossvalue = float(parts[8]) # Loss
            
            # Take only the round values 
            hundred = list(range(0,100,resolution))
            if completed in hundred:
                progress.append(epoch + completed/100)
                accuracy.append(accurate)
                loss.append(lossvalue)
            
    file_input.close()

    progress = progress[:int(epochRange/100*len(progress))]
    accuracy = accuracy[:int(epochRange/100*len(accuracy))]
    loss = loss[:int(epochRange/100*len(loss))]
    
    # Plot the accuracy
    plt.clf()
    plt.ylim(ymax = 100, ymin = 0) #comment
    plt.plot(progress, accuracy,color = 'b', )
    plt.ylabel('Accuracy %')
    plt.xlabel('Epoch')
    plt.savefig(Dir + 'Accuracy.png')
    
    # Plot the loss
    plt.clf()
    plt.plot(progress, loss, color = 'r')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.savefig(Dir + 'Loss.png')
    
    
#%% ROC DIAGRAMS    

def readDict(filePath):
    
    # It reads a json file with the information of the test results that includes:
        # test image names
        # CNN predicted label for each image
        # True label for each image
        # label prediction probability for each prediction
    
    with open(filePath) as dataFile:    
        Dic = json.load(dataFile) # Load the data (the format is included)

    return Dic # Variable


def createROC_ttbar(Dic):
    
    # It creates a histogram: Samples vs ttbar class probability
    
    # Access to the variable Dic information
    
    pred_lab = Dic['pred_lab']
    pred_prob = Dic['pred_prob']
    #y_train = Dic['y_train']
    x_train = Dic['x_train']
    
    # Empty list where the probability values will be stored
    
    class0 = [] # Drell-Yan
    class1 = [] # ttbar
    class2 = [] # W+jets
    
    for n in range(0, len(pred_lab)):
        i = pred_lab[n].index(1) # class 1 ttbar event
        name = x_train[n] # name of the file
        if 'TT' in name:
            class1.append(pred_prob[n][i]) #ttbar
        elif 'W' in name:
            class2.append(pred_prob[n][i]) #Wjets
        elif 'DY' in name: 
            class0.append(pred_prob[n][i]) #DY
            
    print("D-Y: "+str(len(class0)), "ttbar: " +str(len(class1)), "Wjets :" + str(len(class2)))
    
    ### Non log scale
    plt.clf()
    plt.hist([class0, class2], bins = np.linspace(0,1,51), stacked = True, alpha = 0.5, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$"])
    plt.hist(class1, color = 'k', bins = np.linspace(0,1,51), alpha = 0.3, label = r"$t\bar t$")
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t\bar t$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/ttbar-ROCDiagram-linear.png', dpi = 600)
    
    ### Log scale
    
    plt.clf()
    plt.hist([class0, class2], log = True, bins = np.linspace(0,1,51), stacked = True, alpha = 0.5, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$"])
    plt.hist(class1, log = True, color = 'k', bins = np.linspace(0,1,51), alpha = 0.3, label = r"$t\bar t$")
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t\bar t$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/ttbar-ROCDiagram-log.png', dpi = 600)


    ### Normalized diagram
    
    ttbar_xsec = 100.91520690917969
    DY_xsec = 2432.308349609375
    Wjets_xsec = 25842.931640625
    
    ttbar_N =3701947
    DY_N = 36209629
    Wjets_N =81345381
    
    
    weights_B = [[DY_xsec*2714/DY_N]*len(class0), [Wjets_xsec*2714/Wjets_N]*len(class2)]
    weights_S = [ttbar_xsec*2714/ttbar_N]*len(class1)
    
    plt.clf()
    plt.hist([class0, class2], log = True, weights = weights_B, bins = np.linspace(0,1,51), stacked = True, alpha = 0.5, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$"])
    plt.hist(class1, log = True, weights = weights_S, color = 'k', bins = np.linspace(0,1,51), alpha = 0.3, label = r"$t\bar t$")
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t\bar t$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/ttbar-ROCDiagram-normalized-log.png', dpi = 600)
    
    

def createROC_ttprime(Dic):
    
    pred_lab = Dic['pred_lab']
    pred_prob = Dic['pred_prob']
    #y_train = Dic['y_train']
    x_train = Dic['x_train'] # Image paths
    
    class1 = [] #Drell-Yan
    class2 = [] #Wjets
    class3 = [] #ttbar
    class0 = [] #ttprime
    
    for n in range(0, len(pred_lab)):
        i = pred_lab[n].index(0)
        name = x_train[n][43:] #skip the path
        if name[0] == 'T':
            class3.append(pred_prob[n][i])
        elif name[0] == 'W':
            class2.append(pred_prob[n][i])
        elif name[0] == 'D': 
            class1.append(pred_prob[n][i])
        elif name[0] == 'S':
            class0.append(pred_prob[n][i])
            
    print("ttprime: "+str(len(class0)), "D-Y: " +str(len(class1)), "Wjets :" + str(len(class2)), "ttbar: " + str(len(class3)))
    
    ### Non log scale
    plt.clf()
    plt.hist([class1, class2, class3], bins = np.linspace(0,1,51), stacked = True, alpha = 0.5, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$", r"$t\bar t$"])
    plt.hist(class0, color = 'k', bins = np.linspace(0,1,51), alpha = 0.3, label = r"$t'\bar t'$")
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t'\bar t'$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/ttprime-ROCDiagram-linear.png', dpi = 600)
    
    ### Log scale
    
    plt.clf()
    plt.hist([class1, class2, class3], log = True, bins = np.linspace(0,1,51), stacked = True, alpha = 0.5, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$", r"$t\bar t$"])
    plt.hist(class0, log = True, color = 'k', bins = np.linspace(0,1,51), alpha = 0.3, label = r"$t'\bar t'$")
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t'\bar t'$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/ttprime-ROCDiagram-log.png', dpi = 600)
            
    ########## Normalized diagram ############
    
    ttprime_xsec = 3.296245813369751
    ttbar_xsec = 100.91520690917969
    DY_xsec = 2432.308349609375
    Wjets_xsec = 25842.931640625
    
    ttprime_N = 305160
    ttbar_N =3701947
    DY_N = 36209629
    Wjets_N =81345381
    
    
    
    
    weights_B = [[DY_xsec*2714/DY_N]*len(class1), [Wjets_xsec*2714/Wjets_N]*len(class2), [ttbar_xsec*2714/ttbar_N]*len(class3)]
    weights_S = [ttprime_xsec*2714/ttprime_N]*len(class0)
    
    plt.clf()
    plt.hist([class1, class2, class3], log = True, weights = weights_B, bins = np.linspace(0,1,51), stacked = True, alpha = 0.5, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$", r"$t\bar t$"])
    plt.hist(class0, log = True, weights = weights_S, color = 'k', bins = np.linspace(0,1,51), alpha = 0.3, label = r"$t'\bar t'$")
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t'\bar t'$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/ttprime-ROCDiagram-normalized-log.png', dpi = 600)
    
    
def createROC_ttprimewithdata(DicMC, DicData, normedVar):
    
    # It creates a histogram: Samples vs ttprime class probability
    
    # Access to the variables Dic information:
        # DicMC: Samples information
        # DicData: Data information
    
    pred_lab = DicMC['pred_lab']
    pred_prob = DicMC['pred_prob']
    #y_train = Dic['y_train']
    x_train = DicMC['x_train'] # Image paths
    
    pred_labD = DicData['pred_lab']
    pred_probD = DicData['pred_prob']
    #y_train = Dic['y_train']
    
    # Empty variables where probability values will be added
    
    class1 = [] #Drell-Yan
    class2 = [] #Wjets
    class3 = [] #ttbar
    class0 = [] #ttprime
    classD = [] #Data
    
    # Store the probability values:
             
    for n in range(0, len(pred_lab)):
        i = pred_lab[n].index(0) # index 0 because 0 is ttprime class
        name = x_train[n]
        if 'TT' in name:
            class3.append(pred_prob[n][i]) #ttbar
        elif 'W' in name:
            class2.append(pred_prob[n][i]) #Wjets
        elif 'DY' in name: 
            class1.append(pred_prob[n][i]) #DY
        elif 'S' in name:
            class0.append(pred_prob[n][i]) #Signal: ttprime
            
    for n in range(0,len(pred_labD)):
        i = pred_labD[n].index(0) # index 0 because 0 is ttprime class
        classD.append(pred_probD[n][i])
            
    print("ttprime: "+str(len(class0)), "D-Y: " +str(len(class1)), "Wjets :" + str(len(class2)), "ttbar: " + str(len(class3)))
    
    ### Non log scale diagram
    plt.clf()
    plt.hist([class1, class2, class3], bins = np.linspace(0,1,51), stacked = True, alpha = 0.5, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$", r"$t\bar t$"])
    plt.hist(class0, color = 'k', bins = np.linspace(0,1,51), alpha = 0.3, label = r"$t'\bar t'$")
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t'\bar t'$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/ttprime-ROCDiagram-linear.png', dpi = 600)
    
    ### Log scale diagram
    
    plt.clf()
    plt.hist([class1, class2, class3], log = True, bins = np.linspace(0,1,51), stacked = True, alpha = 0.5, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$", r"$t\bar t$"])
    plt.hist(class0, log = True, color = 'k', bins = np.linspace(0,1,51), alpha = 0.3, label = r"$t'\bar t'$")
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t'\bar t'$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/ttprime-ROCDiagram-log.png', dpi = 600)
            
    ########## Normalized diagram ############
    
    # Cross section values
    
    ttprime_xsec = 3.296245813369751
    ttbar_xsec = 100.91520690917969
    DY_xsec = 2432.308349609375
    Wjets_xsec = 25842.931640625
    
    # Total number of samples
    
    ttprime_N = 305160
    ttbar_N =3701947
    DY_N = 36209629
    Wjets_N =81345381
    
    lumi = 2714
    
    # Weights (applie to every event)
    
    w_ttprime = ttprime_xsec*lumi/(ttprime_N) 
    w_ttbar = ttbar_xsec*lumi/(ttbar_N)
    w_DY = DY_xsec*lumi/(DY_N)
    w_Wjets = Wjets_xsec*lumi/(Wjets_N)
    
    weights_B = [[w_DY]*len(class1), [w_Wjets]*len(class2), [w_ttbar]*len(class3)] 
    weights_S = [w_ttprime]*len(class0)
    
    # Histogram
    
    plt.clf()
    plt.hist([class1, class2, class3], normed = normedVar, log = True, weights = weights_B, bins = np.linspace(0,1,51), stacked = True, alpha = 1, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$", r"$t\bar t$"])
    plt.hist(class0, log = True, weights = weights_S, color = 'k', bins = np.linspace(0,1,51), alpha = 0.3, label = r"$t'\bar t'$")
    n, bins, patches = plt.hist(classD, normed = normedVar, log = True, color = 'w', bins = np.linspace(0,1,51), alpha = 0)
    bins_mean = [0.5 * (bins[i] + bins[i+1]) for i in range(len(n))]
    plt.plot(bins_mean, n, color = 'k', linestyle = '-', marker = 'x', label = r'$Data$')
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t'\bar t'$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/data-ROCDiagram-normalized-log.png', dpi = 600)
    
    
    
def createROC_ttbarwithdata(DicMC, DicData, normedVar):
    
    # It creates a histogram: Samples vs ttbar class probability
    
    # Access to the variables Dic information:
        # DicMC: Samples information
        # DicData: Data information
    
    pred_lab = DicMC['pred_lab']
    pred_prob = DicMC['pred_prob']
    #y_train = Dic['y_train']
    x_train = DicMC['x_train']
    
    pred_labD = DicData['pred_lab']
    pred_probD = DicData['pred_prob']
    #y_train = Dic['y_train']
    
    # Empty variables where probability values will be added
    
    class0 = [] # Drell-Yan
    class1 = [] # ttbar
    class2 = [] # W+jets
    classD = [] #Data
    
    # Store the probability values:
    
    for n in range(0, len(pred_lab)):
        i = pred_lab[n].index(1) # class 1 ttbar event
        name = x_train[n] #skip the path
        if 'TT' in name:
            class1.append(pred_prob[n][i]) #ttbar
        elif 'W' in name:
            class2.append(pred_prob[n][i]) #Wjets
        elif 'DY' in name: 
            class0.append(pred_prob[n][i]) #DY
    
            
    for n in range(0,len(pred_labD)):
        i = pred_labD[n].index(1)
        classD.append(pred_probD[n][i])
            
    print("ttbar: "+str(len(class1)), "D-Y: " +str(len(class0)), "Wjets :" + str(len(class2)))
    
            
    ########## Normalized diagram ############
    
    # Cross section values
    
    ttbar_xsec = 100.91520690917969
    DY_xsec = 2432.308349609375
    Wjets_xsec = 25842.931640625
    
    # Total number of samples
    
    ttbar_N =3701947
    DY_N = 36209629
    Wjets_N =81345381
    
    lumi = 2714
    
    # Weights (applie to every event)
    
    w_ttbar = ttbar_xsec*lumi/(ttbar_N)
    w_DY = DY_xsec*lumi/(DY_N)
    w_Wjets = Wjets_xsec*lumi/(Wjets_N)
    
    weights_B = [[w_DY]*len(class0), [w_Wjets]*len(class2), [w_ttbar]*len(class1)] 
    
    plt.clf()
    plt.hist([class0, class2, class1], normed = normedVar, log = True, weights = weights_B, bins = np.linspace(0,1,51), stacked = True, alpha = 1, label = [r"$\mathit{Drell-Yan}$", r"$W+jets$", r"$t\bar t$"])
    n, bins, patches = plt.hist(classD, normed = normedVar, log = True, color = 'w', bins = np.linspace(0,1,51), alpha = 0)
    bins_mean = [0.5 * (bins[i] + bins[i+1]) for i in range(len(n))]
    plt.plot(bins_mean, n, color = 'k', linestyle = '-', marker = 'x', label = r'$Data$')
    
    plt.legend(loc='upper center')
    plt.xlabel(r"$t\bar t$ probability")
    plt.ylabel('Samples')
    plt.savefig('ROC/Probabilities/Diagrams/back-ROCDiagram-normalized-log.png', dpi = 600)
    
    
  