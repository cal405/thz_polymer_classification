import numpy as np
import pandas as pd
import os
import csv
from natsort import natsorted
import matplotlib.pyplot as plt

def feature_extraction(pathGetData='ml/train/data', pathOutput='ml/train/featureFile.csv'):
    '''
    This function reads the whole dir in pathGetData and dumps the information
    that it gets from the filename (plastic type) and the features specified in
    the body of the function. Saves file at pathOutput.
    '''

    #Initial config
    filenames=natsorted(os.listdir(pathGetData))
    labels=list()

    #Features to extract
    nAt2_3THz=list()
    alphaAt2_3THz=list()
    alphaStdDevfrom0_5to2_5THz=list()
    nStdDevfrom0_5to2_5THz=list()
    alphaAvgfrom0_5to1_5THz=list()
    alphaAt1_3THz=list()

    #Extracting features 
    for filename in filenames:
        #Loading data into memory
        sampleName=filename.split('.')[-2]
        if sampleName[0]=='1':
            labels.append('PET')
        elif sampleName[0]=='5':
            labels.append('PP')
        elif sampleName[0]=='2':
            labels.append('HDPE')
        elif sampleName[0]=='4':
            labels.append('LDPE')
        elif sampleName[0]=='6':
            labels.append('PS')
        elif sampleName[0]=='3':
            labels.append('PVC')
        dataframe=np.genfromtxt(pathGetData+'/'+filename, delimiter=',')
        dataframe=dataframe[~np.isnan(dataframe).any(axis=1), :]

        #Here we define where we want to get the data from
        # n and alpha at 2.3THz
        findSpot2_3THz=np.where(dataframe[:,0]==2.2304685965489504)
        nAt2_3THz.append(dataframe[findSpot2_3THz[0],1][0])
        alphaAt2_3THz.append(dataframe[findSpot2_3THz[0],2][0])
        # n and alpha from 0.5 to 2.5 THz
        startSpot0_5THz=np.where(dataframe[:,0]==0.500817154756336)
        endSpot2_5THz=np.where(dataframe[:,0]==2.50042125801517)
        alphaStdDevfrom0_5to2_5THz.append(np.std(dataframe[startSpot0_5THz[0]:endSpot2_5THz[0],2]))
        nStdDevfrom0_5to2_5THz.append(np.std(dataframe[startSpot0_5THz[0]:endSpot2_5THz[0],1]))
        # alpha from 1.5 to 2.5 THz
        endSpot1_5THz=np.where(dataframe[:,0]==1.5000084537580014)
        alphaAvgfrom0_5to1_5THz.append(np.mean(dataframe[startSpot0_5THz[0]:endSpot1_5THz[0],2]))
        # alpha at 1.3 THz
        findSpot1_3THz=np.where(dataframe[:,0]==1.3002923444832186)
        alphaAt1_3THz.append(dataframe[findSpot1_3THz[0],2][0])

    #Loading data  into temp dictionary
    data={'Category':labels,
        'n at 2_3THz':nAt2_3THz,
        'alpha at 2_3THz':alphaAt2_3THz,
        'alphaStdDevfrom0_5to2_5THz':alphaStdDevfrom0_5to2_5THz,
        'nStdDevfrom0_5to2_5THz':nStdDevfrom0_5to2_5THz,
        'alphaAvgfrom0_5to1_5THz':alphaAvgfrom0_5to1_5THz,
        'alpha at 1_3THz':alphaAt1_3THz}

    #Dumping all data to file
    df = pd.DataFrame.from_dict(data)
    df.to_csv(pathOutput,index=False,header=True, sep=',')

#Plotting some samples
def plot_sample(dir_path):
    f1, f2 =plt.figure(), plt.figure()
    af1=f1.add_subplot(111)
    af2=f2.add_subplot(111)
    dirList=natsorted(os.listdir(dir_path))
    for nfile in dirList:
        filePath=os.path.join(dir_path,nfile)
        tArray=[list(),list(),list()]
        with open(filePath) as csvfile:
            csvreader =  csv.reader(csvfile, delimiter = ',' )
            next(csvreader)
            for row in csvreader:
                tArray[0].append(float(row[0]))
                tArray[1].append(float(row[1]))
                tArray[2].append(float(row[2]))
            
        af1.plot(tArray[0],tArray[1],
        linewidth=2.0, label=nfile, linestyle='-')
        af2.plot(tArray[0],tArray[2],
        linewidth=2.0, label=nfile, linestyle='-')

    
        
        af1.set_xlim([0.3,2.5])
        af1.set_ylim([0,3])
        af1.set_ylabel('Refractive index',fontsize=50)
        af1.set_xlabel('Frequency (THz)',fontsize=50)
        af1.set_xticks(np.arange(0.3, 2.6, step=0.1))
        af1.grid(False)
        af2.set_xlim([0.3,2.5])
        af2.set_ylim([-20,200])
        af2.set_ylabel('Absorption (1/cm)',fontsize=30)
        af2.set_xlabel('Frequency (THz)',fontsize=30)
        af2.set_xticks(np.arange(0.3, 2.6, step=0.1))
        af2.grid(False)
        plt.draw()
    plt.show()





