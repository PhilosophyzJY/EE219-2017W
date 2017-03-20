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
	only6_NMF_NLT()

def print_results(lab_true,lab_pred):

	print("Homogeneity: %0.3f" % metrics.homogeneity_score(lab_true, lab_pred))
	print("Completeness: %0.3f" % metrics.completeness_score(lab_true, lab_pred))
	print("V-measure: %0.3f" % metrics.v_measure_score(lab_true, lab_pred))
	print("Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(lab_true, lab_pred))
	print("Adjusted Mutual Information Score: %.3f" % metrics.adjusted_mutual_info_score(lab_true, lab_pred))
	print metrics.confusion_matrix(lab_true,lab_pred)

def only6_NMF_NLT():

	english_stemmer = Stemmer.Stemmer('en')
	class StemmedTfidfVectorizer(TfidfVectorizer):

		def build_analyzer(self):
			analyzer = super(TfidfVectorizer, self).build_analyzer()
			return lambda doc: english_stemmer.stemWords(analyzer(doc))

	print("Loading 20 newsgroups dataset for all categories...")

	newsgroups = fetch_20newsgroups(subset='all')
	
	print("%d documents" % len(newsgroups.data))
	print("%d categories" % len(newsgroups.target_names))

	print("Creating stemmed TFxIDF representation...")
	t0 = time()

	vect = StemmedTfidfVectorizer(stop_words='english')
	vectors = vect.fit_transform(newsgroups.data) # TFxIDF representation

	print("Done in %fs" % (time() - t0))
	print("n_samples: %d, n_features: %d" % vectors.shape)

	purityMetricsNames = ['Homogeneity', 'Completeness', 'V-measure', 'Adjust Rand-Index', 'Adjusted Mutual Information Score']

	# Reducing the dimensionality with NMF NLT

	nmf_nlt_dim_bank = range(1,21)

	workbook = xlsxwriter.Workbook('part6_pt2_NMF_NLT.xlsx')

	for dims in nmf_nlt_dim_bank:

		print("Implementing NMF of dimension %d on data..." % dims)
		nmf_ = NMF(n_components=dims) # alpha value? l1 value?
		nmf_data = nmf_.fit_transform(vectors)
		print("Done.")

		print("Implementing non-linear transform on data...")
		offset = 0.001
		nmf_data_off=np.add(nmf_data,offset)
		log_nmf_data=np.log(nmf_data_off)
		print("Done.")

		k = 6
		km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)

		print("Clustering sparse data with %s" % km)
		t0 = time()
		km.fit(log_nmf_data)
		print("done in %0.3fs" % (time() - t0))

		print_results(newsgroups.target,km.labels_)
		purityMetrics = [metrics.homogeneity_score(newsgroups.target, km.labels_), metrics.completeness_score(newsgroups.target, km.labels_),metrics.v_measure_score(newsgroups.target, km.labels_),metrics.adjusted_rand_score(newsgroups.target, km.labels_),metrics.adjusted_mutual_info_score(newsgroups.target, km.labels_)]

		# Writing to .xlsx file (For Stats)
		worksheet = workbook.add_worksheet()

		row = 0
		col = 0

		worksheet.write(row,col,'Dimension')
		worksheet.write(row,col+1,dims)

		metric_list = dict(zip(purityMetricsNames,purityMetrics))
		pprint(dict(metric_list))

		for key in metric_list.keys():
			row += 1
			worksheet.write(row,col+11,key)
			worksheet.write(row,col+12,metric_list[key])

if __name__ == "__main__":
    main()