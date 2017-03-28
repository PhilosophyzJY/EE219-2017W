import json
import xlsxwriter
from math import floor
def main():
	
	# Change this line for the hashtag #
	AverageTweetsPerHour('tweets_#nfl.txt')

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
	
	# Change this line for the hashtag #
	print 'For #nfl, the stats are: \n'
	
	print 'Total number of tweets = ', length
	print 'Average number of tweets per hour = ', avgTweetsPerHour
	print 'Average number of followers per tweet = ', avgFollowersPerTweet
	print 'Average number of retweets per tweet = ', avgRetweetsPerTweet
	
	# Create histogram #
	histo = []
	
	for n in range(1,max(byHour)+1):
		histo.append(byHour.count(n))
	
	# Change this line for the hashtag #
	workbook = xlsxwriter.Workbook('NFL Histogram.xlsx')
	
	worksheet = workbook.add_worksheet()
	
	col = 0
	for row, data in enumerate(histo):
		worksheet.write_number(row,col,data)

	workbook.close()
	
if __name__ == '__main__':
	main()

