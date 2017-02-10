#Project2 part b 
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.stem.lancaster import LancasterStemmer



#importing data
#This time instead of importing 8 listed classes, imports all 20 classes
twenty_train = fetch_20newsgroups(subset='train', shuffle=True, random_state=42)
twenty_test = fetch_20newsgroups(subset='test', shuffle=True, random_state=42)

print 'the twenty classes are: \n'
print twenty_train.target_names
print '\n'

#http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
#>>> from nltk import word_tokenize
#>>> from nltk.stem import WordNetLemmatizer
#>>> class LemmaTokenizer(object):
#...     def __init__(self):
#...         self.wnl = WordNetLemmatizer()
#...     def __call__(self, doc):
#...         return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]
#words filter
class tk(object):  
    def __init__(self):
        self.tok=RegexpTokenizer(r'\b([a-zA-Z]+)\b')
        self.stemmer = LancasterStemmer()
    def __call__(self, doc):
        return [self.stemmer.stem(s) for s in self.tok.tokenize(doc)]  


    # define the word list to be ignored
    stop_words=text.ENGLISH_STOP_WORDS




#assigning countvectornizer function to vectorizer, which converts a collection of text documnets to a matrix of token counts
#ignore the words that appear less than once
vectorizer = CountVectorizer(min_df=1)


# converting to matrix of token counts


count_vect=CountVectorizer(stop_words=text.ENGLISH_STOP_WORDS,
                           min_df=1,
                           tokenizer=tk())
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



tfidf_transformer=TfidfTransformer()
X_train_tfidf= tfidf_transformer.fit_transform(X_train_counts)

#check matrix dimension
print 'the dimension of Tfidf matrix is:\n'
print X_train_tfidf.shape
#This gives 11314 documents in total and 54358 words.

#check the first 30 rows and 10 columns
#X_train_tfidf.toarray()[:30,:10]
#each row corresponding to a documnents and each column corresponding to the inportance of a word to that document