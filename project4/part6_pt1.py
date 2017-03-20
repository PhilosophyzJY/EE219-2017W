from sklearn.datasets import fetch_20newsgroups as f20
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
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
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix

english_stemmer = Stemmer.Stemmer('en')
class StemmedTfidfVectorizer(TfidfVectorizer):

    def build_analyzer(self):
      analyzer = super(TfidfVectorizer, self).build_analyzer()
      return lambda doc: english_stemmer.stemWords(analyzer(doc))

#loading all the data
cats = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware','comp.sys.mac.hardware', 'comp.windows.x', 
        'rec.autos', 'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey',
        'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space',
        'misc.forsale',
        'talk.politics.misc','talk.politics.guns','talk.politics.mideast',
        'talk.religion.misc','alt.atheism','soc.religion.christian']

print("Loading 20 newsgroups dataset for categories:")
print '\n'
print list(cats) 
print '\n'

traindata = f20(subset='all')

print "%d documents" % len(traindata.data)
print "%d categories" % len(traindata.target_names)
print '\n'

print"Creating stemmed TFxIDF representation..."
t0 = time()

vect = StemmedTfidfVectorizer(stop_words='english')
vectors = vect.fit_transform(traindata.data) # TFxIDF representation

print"Done in %fs" % (time() - t0)
print"n_samples: %d, n_features: %d" % vectors.shape
print'\n'


# Changing the labels from 0-20 to 0-5
print 'changing labels'
t0 = time()
labels_20 = traindata.target
labels_6 = []
for mark in labels_20:
  if mark <= 4:
	labels_6.append(0)
  if mark > 4 and mark <= 8:
	labels_6.append(1)
  if mark > 8 and mark <= 12:
        labels_6.append(2)
  if mark >12 and mark <=13:
        labels_6.append(3)
  if mark >13 and mark <= 16:
        labels_6.append(4)
  if mark >16 and mark <= 19:
        labels_6.append(5)

print"Done in %fs" % (time() - t0)
print '\n'
metric_list = {}
purityMetricsNames = ['Homogeneity', 'Completeness', 'V-measure', 'Adjust Rand-Index', 'Adjusted Mutual Information Score']

#normalizing NMF data
normalizer = Normalizer(copy=False)
print 'performing normalization on NMF data'

#trying different dimension normalized NMF data and grouping into 20 classes
workbook = xlsxwriter.Workbook('part6_pt1.xlsx')
threshold = np.arange(1,21)
for dimension  in threshold:
  print "normalized NMF dimension= %d" % dimension

  rnmf = NMF(n_components=dimension, init='random', random_state=0)
  rnorm_nmf = make_pipeline(rnmf, normalizer)
  rnorm_nmfdata=rnorm_nmf.fit_transform(vectors)
  km = KMeans(n_clusters=6, init='k-means++', max_iter=100, n_init=1)
  km.fit(rnorm_nmfdata)
  print "Homogeneity: %0.3f" % metrics.homogeneity_score(labels_6, km.labels_)
  print "Completeness: %0.3f" % metrics.completeness_score(labels_6, km.labels_)
  print "V-measure: %0.3f" % metrics.v_measure_score(labels_6, km.labels_)
  print "Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(labels_6, km.labels_)
  print "confusion matrix: \n"
  print confusion_matrix(labels_6, km.labels_)
  print '\n'
  purityMetrics = [metrics.homogeneity_score(labels_6, km.labels_), metrics.completeness_score(labels_6, km.labels_),metrics.v_measure_score(labels_6, km.labels_),metrics.adjusted_rand_score(labels_6, km.labels_),metrics.adjusted_mutual_info_score(labels_6, km.labels_)]
  metric_list = dict(zip(purityMetricsNames,purityMetrics))

  worksheet = workbook.add_worksheet()
  row = 0
  col = 0
  for key in metric_list.keys():
    row += 1
    worksheet.write(row,col+11,key)
    worksheet.write(row,col+12,metric_list[key])
workbook.close()



