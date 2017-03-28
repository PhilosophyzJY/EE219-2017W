import json
import math
import datetime
import xlsxwriter
import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn import linear_model
from sklearn.metrics import mean_squared_error

def main():
    
    # Change this line for the hashtags to be included #
    # gohawks should be first when using all hashtags #
    hashtags = ['tweets_#gohawks.txt']
     
    # Construct observations and targets #
    excelname = ConstructData(hashtags,'gohawksNew.xlsx',973)

    # Importing data from ConstructData #
    data = pd.ExcelFile(excelname)
    sheet = data.parse(0)

    # Separating observations from targets #
    obs = []
    featnum = 15
    
    for n in range(0,len(sheet)):
        obs.append(sheet.iloc[n,:featnum])
    
    obs = np.asarray(obs)     
    target = np.asarray(sheet.iloc[:,featnum])

    # Generating model #
    lin = linear_model.LinearRegression()

    # Fitting model #
    lin.fit(obs,target)
    prediction = lin.predict(obs)
    
    # Calculating Error #
    RMSE = math.sqrt(mean_squared_error(target,prediction))

    print 'The RMSE of #gohawks with more features is :', RMSE


def ConstructData(hashtags,excelname,span):
    
    length = 0
    
    byHour = [0]*span
    retweets = [0]*span
    followers = [0]*span
    maxfl = [0]*span
    favorites = [0]*span
    rankingScore = [0]*span
    citations = [0]*span
    impression = [0]*span
    momentum = [0]*span
    
    uniUser = defaultdict(list)
    
    calcHour = []
    
    # Read in tweets, line by line #
    for hashtag in hashtags:
        
        print hashtag
        
        for line in open(hashtag, 'r'):
            thisTweet = json.loads(line)
            length = length + 1
        
            if length == 1:
                begin = float(thisTweet['firstpost_date'])
        
            current = float(thisTweet['firstpost_date'])
            elapsed = math.floor((current - begin) / 3600)
            hour = int(elapsed)

            byHour[hour] = byHour[hour] + 1
            retweets[hour] = retweets[hour] + thisTweet['tweet']['retweet_count']
            followers[hour] = followers[hour] + thisTweet['tweet']['user']['followers_count']
            favorites[hour] = favorites[hour] + thisTweet['tweet']['favorite_count']
            rankingScore[hour] = rankingScore[hour] + thisTweet['metrics']['ranking_score']
            citations[hour] = citations[hour] + thisTweet['metrics']['citations']['total']
            impression[hour] = impression[hour] + thisTweet['metrics']['impressions']
            momentum[hour] = momentum[hour] + thisTweet['metrics']['momentum']
            
            uniUser[hour].append(thisTweet['tweet']['user']['id'])
            
            if thisTweet['tweet']['user']['followers_count'] > maxfl[hour]:
                maxfl[hour] = thisTweet['tweet']['user']['followers_count']
    
    # Construct data #
    data = []
    
    start = datetime.datetime.fromtimestamp(begin)
    hr = start.hour
    
    for n in range(1,span+1):
        calcHour.append(hr)
        
        hr += 1
        
        if hr == 25:
            hr = 1
            
    for n in range(0,span-1):
        
        temp = []
        
        temp.append(byHour[n])
        temp.append(retweets[n])
        temp.append(followers[n])
        temp.append(maxfl[n])
        temp.append(calcHour[n])
        
        temp.append(favorites[n])
                  
        temp.append(rankingScore[n])
        
        if byHour[n] == 0:
            temp.append(0)
         
        if byHour[n] != 0:
            temp.append(rankingScore[n] / byHour[n])
        
        temp.append(citations[n])
        
        if byHour[n] == 0:
            temp.append(0)
         
        if byHour[n] != 0:
            temp.append(citations[n] / byHour[n])        
        
        temp.append(impression[n])
        
        if byHour[n] == 0:
            temp.append(0)
         
        if byHour[n] != 0:
            temp.append(impression[n] / byHour[n])  
                   
        temp.append(momentum[n])
        
        if byHour[n] == 0:
            temp.append(0)
         
        if byHour[n] != 0:
            temp.append(momentum[n] / byHour[n])        
        
        temp.append(len(np.unique(uniUser[n])))
        
        temp.append(byHour[n+1])
        data.append(temp)       

    # Writing to excel file
    workbook = xlsxwriter.Workbook(excelname)
    worksheet = workbook.add_worksheet()

    headers = ['numTweets','numRetweets','sumFollowers','maxFollowers','timeOfDay',
               'sumFavorites','sumRankScore','avgRankScore','sumCitations','avgCitations',
               'sumImpressions','avgImpressions','sumMomentum','avgMomentum','uniqueUsers',
               'tweetsNextHour']
 
    col = 0
    for row, data in enumerate(data):
        worksheet.write_row(row+1,col,data)

    # Adding headers to the data
    row = 0
    for i, data in enumerate(headers):
        worksheet.write(row,col+i,data)
 
    workbook.close() 

    return excelname
   
       
if __name__ == '__main__':
    main()       