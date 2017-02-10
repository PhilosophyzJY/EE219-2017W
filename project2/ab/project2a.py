from sklearn.datasets import fetch_20newsgroups
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


#importing data
categories = ['comp.graphics','comp.os.ms-windows.misc','comp.sys.ibm.pc.hardware','comp.sys.mac.hardware','rec.autos','rec.motorcycles','rec.sport.baseball','rec.sport.hockey']
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
twenty_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42)

#plotting
x=np.arange(0,9,1)

fig1,ax = plt.subplots()
counts, bins, patches = ax.hist(twenty_train.target,x, facecolor='blue', edgecolor='white')
my_xticks=['comp.graphics','comp.os.ms-windows.misc','comp.sys.ibm.pc.hardware','comp.sys.mac.hardware','rec.autos','rec.motorcycles','rec.sport.baseball','rec.sport.hockey']
plt.xticks(x, my_xticks, rotation=35, horizontalalignment='center')

ax.set_xlabel('Topics')
ax.set_ylabel('Number of documents')
plt.title('Number of Documents per Topic')
plt.subplots_adjust(bottom=0.2)
plt.show()

#print target names
print twenty_train.target_names
print len(twenty_train.data)
print len(twenty_train.target)
print len(twenty_train.filenames)
#end of project2 part a


# part b
# Extracting features from text

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text

#assigning countvectornizer function to vectorizer, which converts a collection of text documnets to a matrix of token counts
#ignore the words that appear less than once
vectorizer = CountVectorizer(min_df=1)

# define the word list to be ignored
stop_words=text.ENGLISH_STOP_WORDS

# converting to matrix of token counts
count_vect=CountVectorizer(stop_words=text.ENGLISH_STOP_WORDS,min_df=1)
X_train_counts=count_vect.fit_transform(twenty_train.data)

# X_train_counts.shape gives (4738, 79218) meaning 4738 documents and 79218 words total

#check words and count, here check first 10 words for example:

#from itertools import islice
#def take(m,iterable):
#    return list(islice(iterable,n))

#print 'the first 10 words are:'
#print list(count_vect.vocabulary_keys())[0:10]
#print '\n'

#print 'the first 5 words and their counts are:'
#print take(5, count_vect.vocabulary_.items())
#print '\n'

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer=TfidfTransformer()
X_train_tfidf= tfidf_transformer.fit_transform(X_train_counts)

#check matrix dimension
#X_train_tfidf.shape
#This gives 4732 documents in total and 78911 words.

#check the first 30 rows and 10 columns
#X_train_tfidf.toarray()[:30,:10]
#each row corresponding to a documnents and each column corresponding to the inportance of a word to that document

