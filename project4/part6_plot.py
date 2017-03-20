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



# Customized stemmer
english_stemmer = Stemmer.Stemmer('en')
class StemmedTfidfVectorizer(TfidfVectorizer):

    def build_analyzer(self):
      analyzer = super(TfidfVectorizer, self).build_analyzer()
      return lambda doc: english_stemmer.stemWords(analyzer(doc))

cats = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware','comp.sys.mac.hardware', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey']

print("Loading 20 newsgroups dataset for categories:")
print '\n'
print list(cats) 
print '\n'

traindata = f20(subset='all', categories = cats)

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

# Changing the labels from 0-7 to 0-1
print 'changing labels'
t0 = time()
labels = traindata.target
labels_true = []
for mark in labels:
  if mark <= 3:
	labels_true.append(0)
  else:
	labels_true.append(1)
print"Done in %fs" % (time() - t0)
print '\n'

n=18
print "Implementing NMF on data"
t0 = time()
nnmf = NMF(n_components= n, init='random', random_state=0)
nmfdata= nnmf.fit_transform(vectors)
print"Done in %fs" % (time() - t0)
print '\n'


#using best lambda value
add=0.000183
addnmfdata=np.add(nmfdata,add)
log_nmfdata=np.log(addnmfdata)
km = KMeans(n_clusters=2, init='k-means++', max_iter=100, n_init=1)
km.fit(log_nmfdata)
print "Clustering nonlinear transformed NMF data using K-means"
t0 = time()
km.fit(log_nmfdata)
print "done in %0.3fs" % (time() - t0)
print 'lambda = %f' % add
print "Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, km.labels_)
print "Completeness: %0.3f" % metrics.completeness_score(labels_true, km.labels_)
print "V-measure: %0.3f" % metrics.v_measure_score(labels_true, km.labels_)
print "Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(labels_true, km.labels_)
print "confusion matrix: "
print confusion_matrix(labels_true, km.labels_)
print '\n'

#2D data
nnmf2d = NMF(n_components= 2, init='random', random_state=0)
nmfdata2d= nnmf2d.fit_transform(vectors)
add=0.00015
addnmfdata2d=np.add(nmfdata2d,add)
log_nmfdata2d=np.log(addnmfdata2d)
label_tf=[]
for i in range(len(km.labels_)):
 if labels_true[i]==km.labels_[i]==0:
   #label_tf[i]=0
    label_tf.append(0)
 if labels_true[i]==0 and labels_true[i] != km.labels_[i]:
   #label_tf[i]=1
    label_tf.append(1)
 if labels_true[i]==km.labels_[i]==1:
   #label_tf[i]=2
    label_tf.append(2)
 if labels_true[i]==1 and labels_true[i] != km.labels_[i]:
   #labek_tf[i]=3 
    label_tf.append(3)
#plot 2D data with labels from higher dimension

#kmeans labels on log NMF 2D DATA
plt.figure(3)
plt.scatter(log_nmfdata2d[:,0],log_nmfdata2d[:,1],c=km.labels_)

plt.title('2D Clustering nonlinear transformed (logarithm) nmf data using K-means') 
#ground truth labels on log NMF 2D DATA
plt.figure(4)
plt.scatter(log_nmfdata2d[:,0],log_nmfdata2d[:,1],c=labels_true)
plt.title('2D Clustering nonlinear transformed (logarithm) nmf data ground truth') 

#tp fp tn fn labels on NMF 2D DATA
plt.figure(5)
plt.scatter(nmfdata2d[:,0],nmfdata2d[:,1],c=label_tf)
plt.title('Clustering nmf data tp tn fp fn')
#tp fp tn fn labels on log NMF 2D DATA 
plt.figure(6)
plt.scatter(log_nmfdata2d[:,0],log_nmfdata2d[:,1],c=label_tf)
plt.title('Clustering nonlinear transformed (logarithm) nmf data tp tn fp fn')
plt.show()

