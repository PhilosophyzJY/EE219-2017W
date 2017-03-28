import json
import numpy
import xlsxwriter
import math as mt
from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD as TSVD
from pprint import pprint
import pandas as pd
import csv
from sklearn.metrics import mean_squared_error
import tokenize
import nltk
import Stemmer
from sklearn.svm import SVC
import pickle
from sklearn.model_selection import KFold
from operator import itemgetter
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.metrics import roc_curve 

english_stemmer = Stemmer.Stemmer('en')

class defaultlist(list):
    def __init__(self, fx):
        self._fx = fx
    def __setitem__(self, index, value):
        while len(self) <= index:
            self.append(self._fx())
        list.__setitem__(self, index, value)

class StemmedTfidfVectorizer(TfidfVectorizer):
	def build_analyzer(self):
		analyzer = super(TfidfVectorizer, self).build_analyzer()
		return lambda doc: english_stemmer.stemWords(analyzer(doc))

def main():

	# Pack data set, only needs to be run once
	fanBasePredictorPack('tweets_#superbowl.txt') # Only need to be run once

	# Unpack data set
	with open('tweetText', 'rb') as f:
		tweetText = pickle.load(f)

	with open('tru_loc', 'rb') as f:
		tru_loc = pickle.load(f)

	fanBasePredictor(tweetText,tru_loc)

def fanBasePredictorPack(filename):

	tweets = []
	tweetText = []

	# Keywords that we look for in the location field
	WA_ind = ['Seattle', 'Washington', 'WA', 'Kirkland', 'Spokane','Tacoma','Bellevue','Everett'] # 0
	MA_ind = ['Boston', 'Massachusetts','MA', 'New England', 'Worcester','Lowell','New Bedford','Brockton'] # 1

	loc_ind = WA_ind + MA_ind

	tru_loc = []

	# Sorting through dataset
	for line in open(filename, 'r'):
		thisTweet = json.loads(line)
		location = thisTweet['tweet']['user']['location']

		# Massachusetts
		if location in MA_ind:
			tweetText.append(thisTweet['tweet']['text'])
			tru_loc.append(1)

		# Washington
		if location in WA_ind:
			tweetText.append(thisTweet['tweet']['text'])
			tru_loc.append(0)
	
	# Pickle the data set here
	with open('tweetText', 'wb') as f:
		pickle.dump(tweetText, f, pickle.HIGHEST_PROTOCOL)

	with open('tru_loc','wb') as f:
		pickle.dump(tru_loc, f, pickle.HIGHEST_PROTOCOL)

	print 'Data has been packed for later use.'

def fanBasePredictor(tweetText,tru_loc):

	workbook = xlsxwriter.Workbook('superbowlLocation.xlsx')

	# Training set definition and labels
	trainRatio = 0.80 
	trainSize = int(mt.floor(trainRatio*len(tweetText)))
	tru_loc_train = tru_loc[:trainSize]

	# Testing set definition and labels
	testSize = int(len(tweetText) - trainSize)
	tru_loc_test = tru_loc[-testSize:]

	# pprint(list(tru_loc_test))
	vectorizerTrain = StemmedTfidfVectorizer(stop_words='english')
	vectorsTrain = vectorizerTrain.fit_transform(tweetText[:trainSize])

	vectorizerTest = StemmedTfidfVectorizer(stop_words='english')
	vectorsTest = vectorizerTest.fit_transform(tweetText[-testSize:])

	# Perform LSI
	lsitsvd = TSVD(n_components = 25)

	lsitrain = lsitsvd.fit_transform(vectorsTrain)
	lsitest = lsitsvd.fit_transform(vectorsTest)

	# Create SVM
	svm = SVC(kernel='linear')
	oursvm = svm.fit(lsitrain,tru_loc_train)

	# Compute prediction based on model
	pred_loc = oursvm.predict(lsitest)

	obs = zip(pred_loc,tru_loc_test)

	# Write results out to excel file
	worksheet = workbook.add_worksheet()

	row = 0
	col = 0

	worksheet.write(row,col,'Predictions')
	worksheet.write(row,col+1,'Actuals')

	row = 0
	col = 0	

	for pred, actual in (obs):
		row += 1
		worksheet.write(row,col, pred)
		worksheet.write(row,col+1,actual)
	
	print 'Predictions and Actuals have been written to excel file.'

	# plot ROC curve
	svmscore = oursvm.decision_function(lsitest)
	fpr, tpr, ink = roc_curve(tru_loc_test, svmscore)

	# create array for Excel
	x, y = len(fpr), 2
	roc = [[0 for m in range(x)] for n in range(y)]
 
	for x in range(0, len(fpr)):
		roc[0][x] = fpr[x]
		roc[1][x] = tpr[x]

	# write results to Excel file for plotting and analysis
	workbook = xlsxwriter.Workbook('ROC Curve LSVM.xlsx')
	worksheet = workbook.add_worksheet()
	  
	row = 0
	for col, data in enumerate(roc):
		worksheet.write_column(row,col,data)

	workbook.close()
	
	print 'The ROC data has been written to ROC Curve LSVM.xlsx.'

if __name__ == '__main__':
	main()