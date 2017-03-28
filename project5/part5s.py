import json
import datetime
from math import floor

def main():
    
    # Change this line for the hashtag #
    AverageTweetsPerHour('sample10_period3.txt')


def AverageTweetsPerHour(filename):

    length = 0
    followers = 0.0
    retweets = 0.0
    byHour = []

    for line in open(filename, 'r'):
        thisTweet = json.loads(line)
        length = length + 1
        followers = followers + thisTweet['tweet']['user']['followers_count']
        retweets = retweets + thisTweet['tweet']['retweet_count']
        
        if length == 1:
            begin = float(thisTweet['firstpost_date'])
        
        current = float(thisTweet['firstpost_date'])
        elapsed = floor((current - begin) / 3600)
        hour = int(1 + elapsed)
        byHour.append(hour)
    
    end = float(thisTweet['firstpost_date'])
    
    # Calculate statistics #
    timeS = end - begin
    timeH = timeS / 3600
    
    avgTweetsPerHour = length / timeH
    avgFollowersPerTweet = followers / length
    avgRetweetsPerTweet = retweets / length
    
    print filename
    
    print 'Beginning time =', datetime.datetime.fromtimestamp(begin)
    print 'Ending time =', datetime.datetime.fromtimestamp(end)
    
    print 'Total number of tweets =', length
    print 'Average number of tweets per hour =', avgTweetsPerHour
    print 'Average number of followers per tweet =', avgFollowersPerTweet
    print 'Average number of retweets per tweet =', avgRetweetsPerTweet
    
    
if __name__ == '__main__':
    main()