import json
import datetime
import pandas as pd
import numpy as np
from sklearn import linear_model

# Read in data #
filename = 'allhashtagsNew6.xlsx'
data = pd.ExcelFile(filename)
sheet = data.parse(0)

# Separating observations from targets #
obs = []
featnum = 15

for n in range(0,len(sheet)):
    obs.append(sheet.iloc[n,:featnum])
    
obs = np.asarray(obs)     
target = np.asarray(sheet.iloc[:,featnum])

hrMark = 827

obs1 = obs[:hrMark]
target1 = target[:hrMark]

obs2 = obs[hrMark:hrMark+12]
target2 = target[hrMark:hrMark+12]

obs3 = obs[hrMark+12:]
target3 = target[hrMark+12:] 

# Generating model #
lin = linear_model.LinearRegression()
    
# Fitting model #
# Change based on the period #
testname = 'sample10_period3.txt'
lin.fit(obs3,target3)

numTweets = 0
retweets = 0
followers = 0
maxfl= 0
favorites = 0
rankingScore = 0
citations = 0
impression = 0
momentum = 0
uniUser = []

for line in open(testname, 'r'):
    thisTweet = json.loads(line)
    
    numTweets += 1
    
    retweets += thisTweet['tweet']['retweet_count']
    
    followers += thisTweet['tweet']['user']['followers_count']
    
    if thisTweet['tweet']['user']['followers_count'] > maxfl:
        maxfl = thisTweet['tweet']['user']['followers_count']
    
    favorites += thisTweet['tweet']['favorite_count']
    
    rankingScore += thisTweet['metrics']['ranking_score']
    
    citations += thisTweet['metrics']['citations']['total']
    
    impression += thisTweet['metrics']['impressions']
    
    momentum += thisTweet['metrics']['momentum']
    
    uniUser.append(thisTweet['tweet']['user']['id'])

end = float(thisTweet['firstpost_date'])

enddate = datetime.datetime.fromtimestamp(end)
calcHr = enddate.hour

featureVector = []

# 5 original features over the span of 6 hours now #
featureVector.append(numTweets)
featureVector.append(retweets)
featureVector.append(followers)
featureVector.append(maxfl)
featureVector.append(calcHr)

# Sum of favorites #
featureVector.append(favorites)

# Sum and Avg of rankingScore #
featureVector.append(rankingScore)
featureVector.append(rankingScore/numTweets)

# Sum and Avg of citations #
featureVector.append(citations)
featureVector.append(citations/numTweets)

# Sum and Avg of impressions #
featureVector.append(impression)
featureVector.append(impression/numTweets)

# Sum and Avg of momentum #
featureVector.append(momentum)
featureVector.append(momentum/numTweets)

# Number of unique users over 6 hours #
featureVector.append(len(np.unique(uniUser)))

# Prediction #
featureVector = np.asarray(featureVector)
featureVector = featureVector.reshape(1,-1)
prediction = abs(int(lin.predict(featureVector)))

print testname
print 'Predicted number of tweets is :', prediction
    