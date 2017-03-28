import json
import numpy
import xlsxwriter
from math import floor
from sklearn import linear_model

def main():
    
    # Change this line for the hashtag #
    ConstructData('tweets_#gopatriots.txt')
    
    # Linear Regression using 5 features #
    # Arunav Pls #

def ConstructData(filename):
    
    length = 0
    byHour = []
    retweets = []
    followers = []
    
    # Read in tweets, line by line #
    for line in open(filename, 'r'):
        thisTweet = json.loads(line)
        length =+ 1
        
        if length == 1:
            begin = float(thisTweet['firstpost_date'])
        
        current = float(thisTweet['firstpost_date'])
        elapsed = floor((current - begin) / 3600)
        hour = int(1 + elapsed)
        
        byHour.append(hour)
        retweets.append(thisTweet['tweet']['retweet_count'])  
        followers.append(thisTweet['tweet']['user']['followers_count'])      
        #append extra features jiawen 
    features = []
    
    # Construct feature vector and values #
    for n in range(1,max(byHour)):
        
        rt = 0
        fl = []
        temp = []
        count = 0
        
        # Number of tweets that hour #
        temp.append(byHour.count(n))
        
        # Calculate statistics #
        for x in range(0,length):
            if byHour[x] == n:
                count = count + 1
                rt = rt + retweets[x]
                fl.append(followers[x])
        
        # Total number of retweets that hour #
        temp.append(rt)
        
        # Sum of the number of followers that hour #
        temp.append(sum(fl))
        
        # Maximum number of followers that hour #
        if count != 0:
            temp.append(max(fl))
        
        else:
            temp.append(0) 
            
        # Time of day (1-24) #

        hourMark = n % 24
        
        if hourMark == 0:
            hourMark = 24.0
        
        temp.append(hourMark)
        
        # Add more features here #
        
        # Number of tweets in the next hour #
        temp.append(byHour.count(n+1))
        
        # Construct feature vector + values #
        features.append(temp)
    
    # Change this line for the hashtag #
    workbook = xlsxwriter.Workbook('Data.xlsx')
     
    worksheet = workbook.add_worksheet()
     
    col = 0
    for row, data in enumerate(features):
        worksheet.write_row(row,col,data)
 
    workbook.close() 
       
if __name__ == '__main__':
    main()       
