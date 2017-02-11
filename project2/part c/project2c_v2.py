#part c starts here
#TFxICF significant terms

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


class tk(object):  
    def __init__(self):
        self.tok=RegexpTokenizer('[a-zA-Z]{2,}')
        self.stemmer = LancasterStemmer()
    def __call__(self, doc):
        return [self.stemmer.stem(s) for s in self.tok.tokenize(doc)]  

# converting to matrix of token counts
#get top 10 features

cate_list=['comp.sys.ibm.pc.hardware','comp.sys.mac.hardware','misc.forsale','soc.religion.christian']
   
for category in cate_list:
    categories=[category]
    twenty_train_single = fetch_20newsgroups(subset='train',categories=categories, shuffle=True, random_state=42,remove=('headers','footers','quotes'))
  #count_vect=CountVectorizer(stop_words=text.ENGLISH_STOP_WORDS,min_df=1,tokenizer=tk(),max_features=10)
  #X_train_counts=count_vect.fit_transform(twenty_train_single.data)
  #tfidf_transformer=TfidfTransformer()
  #X_train_tfidf= tfidf_transformer.fit_transform(X_train_counts)
    tfidf = TfidfVectorizer(analyzer='word',tokenizer=tk(), max_features=10, stop_words=text.ENGLISH_STOP_WORDS)
    twenty_train_max_feature=tfidf.fit_transform(twenty_train_single.data)
    print 'in '+category+'the top 10 words are:'
    print tfidf.vocabulary_.keys()



