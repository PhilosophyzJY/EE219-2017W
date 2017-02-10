import math
import pandas as pd
from sklearn.cross_validation import cross_val_predict
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import KFold
import random
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

enc = OneHotEncoder()
fileName = 'network_backup_dataset.csv'
file = open(fileName)
data = []
file.readline()
for line in file:
    element = line.split(',')


    # assigning integer value to each week number
    element[0] = int(element[0])
    # assigning integer value to day of week, 1 to Monday, 2 to Tuesday, 3 to Wednesday...
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday']
    for i in range(len(WEEKDAYS)):
        if element[1] == WEEKDAYS[i]:
            element[1]=i+1
    # Backup Start Time - Hour of Day
    element[2] = int(element[2])
    # Work-Flow-ID replace Work-flow-ID with the # staring from the 10th character for column3
    element[3] = int(element[3][10:])
    # File Name replace the file name with the # starting from the 5th character for column4
    element[4] = int(element[4][5:])
    # Size of Backup (GB)
    element[5] = float(element[5])
    # Backup Time (hour)
    element[6] = int(element[6])
    data.append(element)
random.shuffle(data)
df = pd.DataFrame(data, columns=['week', 'weekday', 'startTime', 'workflowid', 'filename', 'filesize', 'backuptime'])

sizeofbackup = df.filesize

del df['filesize']

onehot = enc.fit_transform(df).toarray()
linr = linear_model.LinearRegression()
lrpredicted = cross_val_predict(linr, onehot, sizeofbackup, cv=10)


#Random Forest
rf = RandomForestRegressor(n_estimators=34, max_depth=11, max_features='auto', warm_start=True, oob_score=True)
RFpredicted = cross_val_predict(rf, onehot, sizeofbackup, cv=10)
rfpredict=rf.fit(df,sizeofbackup)
#giving the importance of each feature
print rf.feature_importances_
#random forest rmse
print 'RMSE of Random Forest Regression', math.sqrt(mean_squared_error(sizeofbackup, RFpredicted))


