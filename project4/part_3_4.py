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

def main():
	# LSI_TFIDF() # This function runs LSI on the data while sweeping across the dimension parameter
	# NMF_NLT_reg_TFIDF() # This function runs NMF with a Log NLT and alpha regularization parameter while sweeping across the dimension parameter
	# NMF_NLT_TFIDF() # This function runs NMF with a Log NLT while sweeping across the dimension parameter
	# NMF_TFIDF() # This function runs just NMF on data while sweeping across the dimension parameter
	NMF_2() # This function is to get a visual sense of the NMF embedding of the data

def NMF_2():

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

	workbook = xlsxwriter.Workbook('partC_NMF.xlsx')

	print("Implementing NMF of dimension 2 on data...")

	nmf_ = NMF(n_components=2) # alpha value? l1 value?
	nmf_data = nmf_.fit_transform(vectors)

	print("Done.")

	print("Implementing non-linear transform on data...")

	offset = 0.001
	nmf_data_off=np.add(nmf_data,offset)
	log_nmfdata=np.log(nmf_data_off)

	print("Done.")

	labels = newsgroups.target
	labels_2 = []

	# Changing the labels from 0-7 to 0-1 
	for mark in labels:
		if mark <= 3:
			labels_2.append(0)
		else:
			labels_2.append(1)

	k = 2

	km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)

	print("Clustering sparse data with %s" % km)
	t0 = time()
	km.fit(nmf_data)
	km.fit(log_nmfdata)
	print("done in %0.3fs" % (time() - t0))

	# Transforming data back
	data2D = km.transform(nmf_data)
	data2D_logarithm =  km.transform(log_nmfdata)

	plt.figure(1)

	plt.subplot(221)
	print("Plotting labels of Kmeans algorithm using NMF")
	plt.title('NMF Dim 2 Kmeans Algorithm with NMF')
	plt.scatter(nmf_data[:,0], nmf_data[:,1], c=km.labels_)
	
	plt.subplot(222)
	print("Plotting ground truth")
	plt.title('True labels of data')
	plt.scatter(nmf_data[:,0], nmf_data[:,1], c=labels_2)

	plt.subplot(223)
	print("Plotting labels of Kmeans algorithm with nonlinear transform NMF")
	plt.title('NMF Dim 2 Kmeans Algorithm Nonlinear transform')
	plt.scatter(log_nmfdata[:,0], log_nmfdata[:,1], c=km.labels_)
	
	plt.subplot(224)
	print("Plotting ground truth with nonlinear transform")
	plt.title('Ground truth, nonlinear transform')
	plt.scatter(log_nmfdata[:,0], log_nmfdata[:,1], c=labels_2)


	plt.show()

	print ("Done.")
	
def NMF_NLT_reg_TFIDF():

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

	workbook = xlsxwriter.Workbook('part3_NMF_NLT.xlsx')

	purityMetricsNames = ['Homogeneity', 'Completeness', 'V-measure', 'Adjust Rand-Index', 'Adjusted Mutual Information Score']

	metric_list = {}

	for i in range(1,21):

		print("Implementing NMF on data...")
		nmf_ = NMF(n_components=i, alpha=0.00018) # 
		nmf_data = nmf_.fit_transform(vectors)
		print("Done.")

		# Applying non-linear transform
		print("Implementing non-linear transform on data...")
		offset = 0.001
		nmf_data_off=np.add(nmf_data,offset)
		log_nmf_data=np.log(nmf_data_off)
		print("Done.")

		labels = newsgroups.target
		labels_2 = []

		# Changing the labels from 0-7 to 0-1 
		for mark in labels:
			if mark <= 3:
				labels_2.append(0)
			else:
				labels_2.append(1)

		k = 2

		km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)

		print("Clustering sparse data with %s" % km)
		t0 = time()
		km.fit(log_nmf_data)
		print("done in %0.3fs" % (time() - t0))

		print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_2, km.labels_))
		print("Completeness: %0.3f" % metrics.completeness_score(labels_2, km.labels_))
		print("V-measure: %0.3f" % metrics.v_measure_score(labels_2, km.labels_))
		print("Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(labels_2, km.labels_))
		print("Adjusted Mutual Information Score: %.3f" % metrics.adjusted_mutual_info_score(labels_2, km.labels_))
		print metrics.confusion_matrix(labels_2,km.labels_)

		purityMetrics = [metrics.homogeneity_score(labels_2, km.labels_), metrics.completeness_score(labels_2, km.labels_),metrics.v_measure_score(labels_2, km.labels_),metrics.adjusted_rand_score(labels_2, km.labels_),metrics.adjusted_mutual_info_score(labels_2, km.labels_)]

		# Writing to .xlsx file (For Confusion Matrix)
		worksheet = workbook.add_worksheet()
		obs = zip(km.labels_,labels_2)

		row = 0
		col = 0

		worksheet.write(row,col,'Predictions')
		worksheet.write(row,col+1,'Actuals')
		worksheet.write(row,col+6,'Dimension')
		worksheet.write(row+1,col+6,i)

		metric_list = dict(zip(purityMetricsNames,purityMetrics))
		pprint(dict(metric_list))

		for key in metric_list.keys():
			row += 1
			worksheet.write(row,col+11,key)
			worksheet.write(row,col+12,metric_list[key])

		row = 0
		col = 0

		for pred, actual in (obs):
			row += 1
			worksheet.write(row,col, pred)
			worksheet.write(row,col+1,actual)

		row = 1

		for things in labels:
			worksheet.write(row,col+2,things)
			row += 1

	workbook.close()

def NMF_NLT_TFIDF():

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

	workbook = xlsxwriter.Workbook('part3_NMF_NLT.xlsx')

	purityMetricsNames = ['Homogeneity', 'Completeness', 'V-measure', 'Adjust Rand-Index', 'Adjusted Mutual Information Score']

	metric_list = {}

	for i in range(1,21):

		print("Implementing NMF on data...")
		nmf_ = NMF(n_components=i) # 
		nmf_data = nmf_.fit_transform(vectors)
		print("Done.")

		# Applying non-linear transform
		print("Implementing non-linear transform on data...")
		offset = 0.001
		nmf_data_off=np.add(nmf_data,offset)
		log_nmf_data=np.log(nmf_data_off)
		print("Done.")

		labels = newsgroups.target
		labels_2 = []

		# Changing the labels from 0-7 to 0-1 
		for mark in labels:
			if mark <= 3:
				labels_2.append(0)
			else:
				labels_2.append(1)

		k = 2

		km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)

		print("Clustering sparse data with %s" % km)
		t0 = time()
		km.fit(log_nmf_data)
		print("done in %0.3fs" % (time() - t0))

		print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_2, km.labels_))
		print("Completeness: %0.3f" % metrics.completeness_score(labels_2, km.labels_))
		print("V-measure: %0.3f" % metrics.v_measure_score(labels_2, km.labels_))
		print("Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(labels_2, km.labels_))
		print("Adjusted Mutual Information Score: %.3f" % metrics.adjusted_mutual_info_score(labels_2, km.labels_))
		print metrics.confusion_matrix(labels_2,km.labels_)

		purityMetrics = [metrics.homogeneity_score(labels_2, km.labels_), metrics.completeness_score(labels_2, km.labels_),metrics.v_measure_score(labels_2, km.labels_),metrics.adjusted_rand_score(labels_2, km.labels_),metrics.adjusted_mutual_info_score(labels_2, km.labels_)]

		# Writing to .xlsx file (For Confusion Matrix)
		worksheet = workbook.add_worksheet()
		obs = zip(km.labels_,labels_2)

		row = 0
		col = 0

		worksheet.write(row,col,'Predictions')
		worksheet.write(row,col+1,'Actuals')
		worksheet.write(row,col+6,'Dimension')
		worksheet.write(row+1,col+6,i)

		metric_list = dict(zip(purityMetricsNames,purityMetrics))
		pprint(dict(metric_list))

		for key in metric_list.keys():
			row += 1
			worksheet.write(row,col+11,key)
			worksheet.write(row,col+12,metric_list[key])

		row = 0
		col = 0

		for pred, actual in (obs):
			row += 1
			worksheet.write(row,col, pred)
			worksheet.write(row,col+1,actual)

		row = 1

		for things in labels:
			worksheet.write(row,col+2,things)
			row += 1

	workbook.close()

def NMF_TFIDF():

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

	workbook = xlsxwriter.Workbook('part3_NMF.xlsx')

	purityMetricsNames = ['Homogeneity', 'Completeness', 'V-measure', 'Adjust Rand-Index', 'Adjusted Mutual Information Score']

	metric_list = {}

	for i in range(1,21):

		print("Implementing NMF on data...")
		nmf_ = NMF(n_components=i) # 
		nmf_data = nmf_.fit_transform(vectors)
		print("Done.")

		labels = newsgroups.target
		labels_2 = []

		# Changing the labels from 0-7 to 0-1 
		for mark in labels:
			if mark <= 3:
				labels_2.append(0)
			else:
				labels_2.append(1)

		k = 2

		km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)

		print("Clustering sparse data with %s" % km)
		t0 = time()
		km.fit(nmf_data)
		print("done in %0.3fs" % (time() - t0))

		print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_2, km.labels_))
		print("Completeness: %0.3f" % metrics.completeness_score(labels_2, km.labels_))
		print("V-measure: %0.3f" % metrics.v_measure_score(labels_2, km.labels_))
		print("Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(labels_2, km.labels_))
		print("Adjusted Mutual Information Score: %.3f" % metrics.adjusted_mutual_info_score(labels_2, km.labels_))
		print metrics.confusion_matrix(labels_2,km.labels_)

		purityMetrics = [metrics.homogeneity_score(labels_2, km.labels_), metrics.completeness_score(labels_2, km.labels_),metrics.v_measure_score(labels_2, km.labels_),metrics.adjusted_rand_score(labels_2, km.labels_),metrics.adjusted_mutual_info_score(labels_2, km.labels_)]

		# Writing to .xlsx file (For Confusion Matrix)
		worksheet = workbook.add_worksheet()
		obs = zip(km.labels_,labels_2)

		row = 0
		col = 0

		worksheet.write(row,col,'Predictions')
		worksheet.write(row,col+1,'Actuals')
		worksheet.write(row,col+6,'Dimension')
		worksheet.write(row+1,col+6,i)

		metric_list = dict(zip(purityMetricsNames,purityMetrics))
		pprint(dict(metric_list))

		for key in metric_list.keys():
			row += 1
			worksheet.write(row,col+11,key)
			worksheet.write(row,col+12,metric_list[key])

		row = 0
		col = 0

		for pred, actual in (obs):
			row += 1
			worksheet.write(row,col, pred)
			worksheet.write(row,col+1,actual)

		row = 1

		for things in labels:
			worksheet.write(row,col+2,things)
			row += 1

	workbook.close()

def LSI_TFIDF():

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

	workbook = xlsxwriter.Workbook('part3_LSI.xlsx')

	purityMetricsNames = ['Homogeneity', 'Completeness', 'V-measure', 'Adjust Rand-Index', 'Adjusted Mutual Information Score']

	metric_list = {}

	for i in range(1,21):

		print("Implementing LSI (TSVD) on data...")
		lsitsvd = TSVD(n_components = i) # What should this be?
		lsidata = lsitsvd.fit_transform(vectors)
		print("Done.")

		labels = newsgroups.target
		labels_2 = []

		# Changing the labels from 0-7 to 0-1 
		for mark in labels:
			if mark <= 3:
				labels_2.append(0)
			else:
				labels_2.append(1)

		k = 2

		km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)

		print("Clustering sparse data with %s" % km)
		t0 = time()
		km.fit(lsidata)
		print("done in %0.3fs" % (time() - t0))

		print("Homogeneity: %0.3f" % max(metrics.homogeneity_score(labels_2, km.labels_), 1-metrics.homogeneity_score(labels_2, km.labels_)))
		print("Completeness: %0.3f" % max(metrics.completeness_score(labels_2, km.labels_), 1-metrics.completeness_score(labels_2, km.labels_)))
		print("V-measure: %0.3f" % max(metrics.v_measure_score(labels_2, km.labels_), 1-metrics.v_measure_score(labels_2, km.labels_)))
		print("Adjusted Rand-Index: %.3f"
	      % max(metrics.adjusted_rand_score(labels_2, km.labels_), 1-metrics.adjusted_rand_score(labels_2, km.labels_)))
		print("Adjusted Mutual Information Score: %.3f"
	      % max(metrics.adjusted_mutual_info_score(labels_2, km.labels_), 1-metrics.adjusted_mutual_info_score(labels_2, km.labels_)))
		print metrics.confusion_matrix(labels_2,km.labels_)

		purityMetrics_2 = [metrics.homogeneity_score(labels_2, km.labels_), metrics.completeness_score(labels_2, km.labels_),metrics.v_measure_score(labels_2, km.labels_),metrics.adjusted_rand_score(labels_2, km.labels_),metrics.adjusted_mutual_info_score(labels_2, km.labels_)]
		
		# Writing to .xlsx file (For Confusion Matrix)
		worksheet = workbook.add_worksheet()
		obs = zip(km.labels_,labels_2)

		row = 0
		col = 0

		worksheet.write(row,col,'Predictions')
		worksheet.write(row,col+1,'Actuals')
		worksheet.write(row,col+6,'Dimension')
		worksheet.write(row+1,col+6,i)

		metric_list_2 = dict(zip(purityMetricsNames,purityMetrics_2))

		for key in metric_list_2.keys():
			row += 1
			worksheet.write(row,col+11,key)
			worksheet.write(row,col+12,metric_list_2[key])


		row = 0
		col = 0

		for pred, actual in (obs):
			row += 1
			worksheet.write(row,col, pred)
			worksheet.write(row,col+1,actual)

		row = 1

		for things in labels:
			worksheet.write(row,col+2,things)
			row += 1

	workbook.close()

if __name__ == "__main__":
    main()