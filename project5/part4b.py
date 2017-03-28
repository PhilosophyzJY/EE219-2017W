import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import KFold

def main():
    
    # Read in data #
    data = pd.ExcelFile('gohawksNew.xlsx')
    sheet = data.parse(0)
    
    featnum = 15
    
    # Separating observations from targets #
    obs = []
    
    for n in range(0,len(sheet)):
        obs.append(sheet.iloc[n,:featnum])
    
    obs = np.asarray(obs)     
    target = np.asarray(sheet.iloc[:,featnum])
    
    # Separate periods #
    hrMark = 835
    
    obs1 = obs[:hrMark]
    target1 = target[:hrMark]

    obs2 = obs[hrMark:hrMark+12]
    target2 = target[hrMark:hrMark+12]

    obs3 = obs[hrMark+12:]
    target3 = target[hrMark+12:] 
    
    # 10 Fold CV for each time period #
    print 'For #gohawks:'
    PerCV(obs1,target1,1)
    PerCV(obs2,target2,2)
    PerCV(obs3,target3,3)
   
def PerCV(obs,target,number):

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
    
    print 'Period', number, ':'
    
    print 'The average prediction error for each part5s is:'
    for n in range(0,len(foldAcc)):
        print foldAcc[n]
        
    print 'The average prediction error over all tests is :', sum(foldAcc) / len(foldAcc)
    print '\n'
    
if __name__ == '__main__':
    main()