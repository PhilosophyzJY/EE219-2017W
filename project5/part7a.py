import json
import math
import xlsxwriter
import numpy as np
import pandas as pd
from decimal import Decimal as dec
from unicodedata import normalize
from sklearn import linear_model
from sklearn.metrics import mean_squared_error

def main():
    
    # Change this line for the hashtags to be included #
    # gohawks should be first when using all hashtags #
    hashtags = ['tweets_#gohawks.txt','tweets_#gopatriots.txt','tweets_#nfl.txt',
                'tweets_#patriots.txt','tweets_#sb49.txt','tweets_#superbowl.txt']
     
    # Construct observations and targets #
    excelname = ConstructData(hashtags,'predictExcitement.xlsx',981)

    # Importing data from ConstructData #
    data = pd.ExcelFile(excelname)
    sheet = data.parse(0)

    # Separating observations from targets #
    obs = []
    featnum = 4
    
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

    print 'The RMSE of predicting excitement is :', RMSE

def ConstructData(hashtags,excelname,span):
    
    length = 0
    
    numTweets = [0]*span
    numExcited = [0]*span
    
    retweets = [0]*span
    followers = [0]*span
    favorites = [0]*span
        
    # Read in tweets, line by line #
    for hashtag in hashtags:
        
        print hashtag
        
        for line in open(hashtag, 'r'):
            
            thisTweet = json.loads(line)
            text = thisTweet['title']
            
            ePunc = 0
            qPunc = 0
            
            # Split up text and filter #
            text = normalize('NFKD',text).encode('ascii','ignore')
            split = text.split()
            sent = []
            
            for n in split:
                
                # Remove hashtags, links, and mentions #
                if '#' in n or 'http' in n or '@' in n:
                    ePunc += n.count('!')
                    qPunc += n.count('?')
                    continue              
                
                sent.append(n)
        
            new = ' '.join(sent)
            length += 1
            
            if length == 1:
                begin = float(thisTweet['firstpost_date'])
        
            current = float(thisTweet['firstpost_date'])
            elapsed = math.floor((current - begin) / 3600)
            hour = int(elapsed)
            
            numTweets[hour] += 1            
            retweets[hour] = retweets[hour] + thisTweet['tweet']['retweet_count']
            followers[hour] = followers[hour] + thisTweet['tweet']['user']['followers_count']
            favorites[hour] = favorites[hour] + thisTweet['tweet']['favorite_count']
                     
            # Number of capital letters in tweet #
            capLet = sum(1 for c in new if c.isupper())
            
            # Percentage of capital letters in tweet
            if len(new) != 0:
                perCapLet = float(capLet) / (len(new))
                
            if len(new) == 0:
                perCapLet = 0
            
            # Number of ! and ? in tweet #
            ePunc += new.count('!')
            qPunc += new.count('?')
            
            # Determine if this user is excited #
            if ePunc >= 1 or qPunc >= 2 or perCapLet >= 0.2:
                numExcited[hour] += 1
            
        # Construct feature vectors and targets #
        data = []
        for n in range(0,span-1):
            temp = []
            
            if numTweets[n] == 0:
                temp.append(0)
                temp.append(0)
                temp.append(0)
                temp.append(0)
                
            if numTweets[n] != 0:
                temp.append(round((dec(numExcited[n]) / numTweets[n]),2))
                temp.append(round((dec(retweets[n]) / numTweets[n]),2))
                temp.append(round((dec(followers[n]) / numTweets[n]),2))
                temp.append(round((dec(favorites[n]) / numTweets[n]),2))
            
            if numTweets[n+1] == 0:
                temp.append(0)
            
            if numTweets[n+1] != 0:
                temp.append(round((dec(numExcited[n+1]) / numTweets[n+1]),2))
            
            data.append(temp)
                   
    # Writing to excel file
    workbook = xlsxwriter.Workbook(excelname)
    worksheet = workbook.add_worksheet()

    headers = ['percExcited','avgRetweets','avgFollowers','avgFavorites',
               'nextExcited']
 
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