from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import Stemmer
from pprint import pprint
import numpy as np
import sys
from time import time
from sklearn import metrics
import xlsxwriter
from itertools import izip
import csv
from sklearn.decomposition import TruncatedSVD as TSVD
import collections as cs
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt

# Customized stemmer
english_stemmer = Stemmer.Stemmer('en')
class StemmedTfidfVectorizer(TfidfVectorizer):

	def build_analyzer(self):
		analyzer = super(TfidfVectorizer, self).build_analyzer()
		return lambda doc: english_stemmer.stemWords(analyzer(doc))

cats = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware','comp.sys.mac.hardware', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey']

print("Loading 20 newsgroups dataset for categories:")
pprint(list(cats))

newsgroups = fetch_20newsgroups(subset='all', categories = cats)

print("%d documents" % len(newsgroups.data))
print("%d categories" % len(newsgroups.target_names))

print("Creating stemmed TFxIDF representation...")
t0 = time()

vect = StemmedTfidfVectorizer(stop_words='english')
vectors = vect.fit_transform(newsgroups.data) # TFxIDF representation

print("Done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % vectors.shape)	

# Changing the labels from 0-7 to 0-1 
labels = newsgroups.target
labels_2 = []

for mark in labels:
	if mark <= 3:
		labels_2.append(0)
	else:
		labels_2.append(1)

k = 2

km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)

print("Clustering sparse data with %s" % km)
t0 = time()
km.fit(vectors)
print("done in %0.3fs" % (time() - t0))

# Printing Statistics of Results 
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_2, km.labels_))
print("Completeness: %0.3f" % metrics.completeness_score(labels_2, km.labels_))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_2, km.labels_))
print("Adjusted Rand-Index: %.3f"
  % metrics.adjusted_rand_score(labels_2, km.labels_))
print("Adjusted Mutual Information Score: %.3f"
  % metrics.adjusted_mutual_info_score(labels_2, km.labels_))
print metrics.confusion_matrix(labels_2, km.labels_)

purityMetricsNames = ['Homogeneity', 'Completeness', 'V-measure', 'Adjust Rand-Index', 'Adjusted Mutual Information Score']
purityMetrics = [metrics.homogeneity_score(labels_2, km.labels_), metrics.completeness_score(labels_2, km.labels_),metrics.v_measure_score(labels_2, km.labels_),metrics.adjusted_rand_score(labels_2, km.labels_),metrics.adjusted_mutual_info_score(labels_2, km.labels_)]

metric_list = {}
metric_list = dict(zip(purityMetricsNames,purityMetrics))

# Writing to .xlsx file
workbook = xlsxwriter.Workbook('part2.xlsx')
worksheet = workbook.add_worksheet()

obs = zip(km.labels_,labels_2)

row = 0
col = 0

for pred, actual in (obs):
	worksheet.write(row,col, pred)
	worksheet.write(row,col+1,actual)
	row += 1

row = 0
col = 0

for key in metric_list.keys():
		row += 1
		worksheet.write(row,col+11,key)
		worksheet.write(row,col+12,metric_list[key])

workbook.close()