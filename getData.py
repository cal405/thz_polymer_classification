import quartz        #Elena Mavrona's algorithm
import csv
import math
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt 
import numpy as np
import scipy.fftpack
import os
from natsort import natsorted

'''
Initial setup
'''

#Where the program should search for files
dataPath='C:\\Users\\cal\\Desktop\\esdldpe'
colorClassified=False
processedDataDir='processed_data/esdldpe'

#Creating figures for plots, they all open once the program reaches plt.show()
# f stands for figure, af for axis from a figure
f1, f2, f3, f4 =plt.figure(), plt.figure(), plt.figure(), plt.figure()
af1=f1.add_subplot(111)
af2=f2.add_subplot(111)
af3=f3.add_subplot(111)
af4=f4.add_subplot(111)

#Some configs for automation
dirList=natsorted(os.listdir(dataPath))
files=list()

#Config for getting sample names & thickness from dir file names
infoDict=dict()
for nnnfile in dirList:
    filepathrel=os.path.join(dataPath,nnnfile)
    files.append(filepathrel)
    splittedString=nnnfile.split('.')
    infoList=splittedString[0].split('_')
    
    #This gives an unique color to each category depending on the filename type (first number)
    if infoList[0]=='ref':
        referenceData=filepathrel
    else:
        identifier=(''.join(infoList[0]+'_'+infoList[2]))
        infoDict[filepathrel]={'name':identifier, 'thickness':int(infoList[3])}
        if int(identifier[0])==1:
            infoDict[filepathrel]['color']='red'
        elif int(identifier[0])==2:
            infoDict[filepathrel]['color']='magenta'
        elif int(identifier[0])==4:
            infoDict[filepathrel]['color']='green'
        elif int(identifier[0])==5:
            infoDict[filepathrel]['color']='blue' 
        else:
            infoDict[filepathrel]['color']='black'


'''
First figure (Electrical Signal vs. Time [ps])
'''

#Get pure signal
dataSpectrum=dict()
counter=0
for nfile in infoDict:
    tArray = [list(),list()]
    with open(nfile) as csvfile:
        csvreader =  csv.reader(csvfile, delimiter = ',' )
        next(csvreader)
        for row in csvreader:
            tArray[0].append(float(row[0]))
            tArray[1].append(float(row[1]))
    dataSpectrum.update({nfile:tArray})
    if colorClassified:
        af1.plot(dataSpectrum[nfile][0],dataSpectrum[nfile][1],
        linewidth=2.0, label=nfile, linestyle='-', color=infoDict[nfile]['color'])
    else:
        af1.plot(dataSpectrum[nfile][0],dataSpectrum[nfile][1],
        linewidth=2.0, label=nfile, linestyle='-')
#Settings for plot
af1.set_xlim([2370,2450])
af1.set_ylabel('E.F.',fontsize=30)
af1.set_xlabel('Time [ps]',fontsize=30)
plt.draw()


'''
Fast Fourier Transform up to 3 THz
'''

#Config for the FFT
tau=np.array(dataSpectrum[files[0]][0])
dt=tau[1400]-tau[0]
df=1/dt
f=np.multiply(df,np.array(range(0,1401)))

#Plot the FFT
for nnfile in infoDict:
    if colorClassified:
        af2.plot(f,abs(scipy.fftpack.fft(dataSpectrum[nnfile][1])),
        linewidth=2.0, label=nnfile, linestyle='-', color=infoDict[nnfile]['color'])
    else:
        af2.plot(f,abs(scipy.fftpack.fft(dataSpectrum[nnfile][1])),
        linewidth=2.0, label=nnfile, linestyle='-')      
#Settings for plot
af2.set_xlim([0,3])
af2.set_ylabel('Spectrum',fontsize=30)
af2.set_xlabel('Frequency (THz)',fontsize=30)
plt.draw()


'''
Algorithm comes into play to calculate the refractive index
'''


#Define here your sample files with thickness in mm
for key in infoDict:
    realPart, imaginaryPart,frequency =quartz(referenceData,key, (float(infoDict[key]['thickness'])/1000.0))
    infoDict[key]['imaginaryPart']=imaginaryPart
    infoDict[key]['frequency']=frequency
    infoDict[key]['realPart']=realPart
    
    #Calculating the absorption
    lamda=3.0e8/frequency
    absorption=-4*math.pi*imaginaryPart/(lamda*100)
    infoDict[key]['absorption']=absorption

    #Saving results to file
    bareFileName=key.split('\\')
    newFileName=os.path.join(processedDataDir,bareFileName[-1])
    with open(newFileName,'w',newline='') as proccsvfile:
        csvwriter=csv.writer(proccsvfile,delimiter=',')
        csvwriter.writerow(['frequency','refractiveIndex','absorption'])
        for row in range(len(frequency)-1):
            csvwriter.writerow([frequency[row+1]*1e-12,realPart[row+1],absorption[row+1]])


#Drawing refractive index plot
for key in infoDict:
    if colorClassified:
        af3.plot((infoDict[key]['frequency'])*1e-12,(infoDict[key]['realPart']),
        linewidth=2.0, label=infoDict[key]['name'], linestyle='-', color=infoDict[key]['color'])
    else:
        af3.plot((infoDict[key]['frequency'])*1e-12,(infoDict[key]['realPart']),
        linewidth=2.0, label=infoDict[key]['name'], linestyle='-')
#Settings for plot
af3.set_xlim([0,3])
af3.set_ylim([-1,3])
af3.set_ylabel('Refractive index',fontsize=30)
af3.set_xlabel('Frequency (THz)',fontsize=30)
af3.legend(loc='upper right',prop={'size':10})
plt.draw()


#Drawing absorption plot
for key in infoDict:
    if colorClassified:
        af4.plot((infoDict[key]['frequency'])*1e-12, infoDict[key]['absorption'],
        linewidth=2.0, label=(infoDict[key]['name']), linestyle='-', color=infoDict[key]['color'])
    else:
        af4.plot((infoDict[key]['frequency'])*1e-12, infoDict[key]['absorption'],
        linewidth=2.0, label=(infoDict[key]['name']), linestyle='-')
#Configure your absorption plot
af4.set_xlim([0,3.0])
af4.set_ylim([-10,200])
af4.set_ylabel('Absorption (1/cm)',fontsize=30)
af4.set_xlabel('Frequency (THz)',fontsize=30)
af4.legend(loc='upper right',prop={'size':10})
plt.draw()


plt.show()
