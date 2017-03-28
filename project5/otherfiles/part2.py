import json
import numpy
import xlsxwriter
from math import floor
from sklearn import linear_model
import json
import numpy as np
import xlsxwriter
from math import floor
from sklearn import linear_model
from datetime import datetime

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
    # extra features

    favorites = []
    userid = []
    accl = []
    rankingscore = []
    impression = []
    momentum = []
    citation_t = []
    hourofday = []
    # Read in tweets, line by line #
    for line in open(filename, 'r'):
        thisTweet = json.loads(line)
        length = length + 1
        
        if length == 1:
            begin = float(thisTweet['firstpost_date'])
        
        current = float(thisTweet['firstpost_date'])
        elapsed = floor((current - begin) / 3600)
        hour = int(1 + elapsed)
        
        byHour.append(hour)
        # append extra features
        favorites.append(thisTweet['tweet']['favorite_count'])
        rankingscore.append(thisTweet['metrics']['ranking_score'])
        impression.append(thisTweet['metrics']['impressions'])
        userid.append(thisTweet['tweet']['user']['id'])
        accl.append(thisTweet['metrics']['acceleration'])
        momentum.append(thisTweet['metrics']['momentum'])
        citation_t.append(thisTweet['metrics']['citations']['total'])
        thour = int(datetime.fromtimestamp(thisTweet['firstpost_date']).strftime("%H"))
        hourofday.append(thour)
        retweets.append(thisTweet['tweet']['retweet_count'])  
        followers.append(thisTweet['tweet']['user']['followers_count'])      


    features = []
    
    # Construct feature vector and values #
    for n in range(1,max(byHour)):
        
        rt = 0
        fl = []
        temp = []
        count = 0
        h_fav = 0
        h_rank = 0
        h_acc = 0
        h_imp = 0
        h_cit = 0
        hourtime = []
        h_mom = 0
        h_id = []
        # Number of tweets that hour #
        temp.append(byHour.count(n))
        
        # Calculate statistics #
        for x in range(0,length):
            if byHour[x] == n:
                count = count + 1
                rt = rt + retweets[x]
                h_fav = h_fav + favorites[x]
                h_acc = h_acc + accl[x]
                h_imp = h_imp + impression[x]
                h_rank = h_rank + rankingscore[x]
                h_cit = h_cit + citation_t[x]
                h_mom = h_mom + momentum[x]
                hourtime.append(hourofday[x])
                h_id.append(userid[x])
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
        calcHour = n % 24
        
        if calcHour == 0:
            calcHour = 24
        
        temp.append(calcHour)
        #total favorites in that hour
        temp.append(h_fav)
        # total acceleration in that hour
        temp.append(h_acc)
        # total impression in that hour
        temp.append(h_imp)
        # total ranking score in that hour
        temp.append(h_rank)
        # total citations in that hour
        temp.append(h_cit)
        # total momentums in that hour
        temp.append(h_mom)
        # total num of users in that hour
        usernum = len(np.unique(h_id))
        temp.append(usernum)
        # avg tweeting time in that hour
        temp.append(np.average(hourtime))
        
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