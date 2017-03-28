import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import KFold

# Read in data #
filename = 'predictExcitement.xlsx'
data = pd.ExcelFile(filename)
sheet = data.parse(0)

print 'For predicting excitement:'

# Separating observations from targets #
obs = []
featnum = 4

for n in range(0,len(sheet)):
    obs.append(sheet.iloc[n,:featnum])
    
obs = np.asarray(obs)     
target = np.asarray(sheet.iloc[:,featnum])

# 10 fold cross validation #
foldAcc = []
kf = KFold(n_splits = 10)
 
for train, test in kf.split(obs,target):
    obsTrain, obsTest = obs[train], obs[test]
    targetTrain, targetTest = target[train], target[test]
    
    # Generating model #
    lin = linear_model.LinearRegression()
    
    # Fitting model and predictions #
    lin.fit(obsTrain,targetTrain)
    prediction = lin.predict(obsTest)
    
    # Calculating average prediction error for current fold #
    foldAcc.append(sum(abs(targetTest - prediction)) / len(targetTest))

print 'The average prediction error for each test is:'
for n in range(0,len(foldAcc)):
    print foldAcc[n]

print 'The average prediction error over all tests is :', sum(foldAcc) / len(foldAcc)