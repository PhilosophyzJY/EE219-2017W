from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk 
import string
from nltk.stem.snowball import SnowballStemmer

#part c w/ word filter version 1 
#need download nltk first:
#nltk.download()

stemmer = SnowballStemmer("english")

def tk(text):
    new_text = re.sub(r'[^A-Za-z]', " ", text)
    tokens =[word for sent in nltk.sent_tokenize(new_text) for word in nltk.word_tokenize(sent)]
    new_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]{2,}', token):
            new_tokens.append(token)     
    stem = [stemmer.stem(s) for s in new_tokens]
    return stem

# converting to matrix of token counts
#get top 10 features



cate_list=['comp.sys.ibm.pc.hardware','comp.sys.mac.hardware','misc.forsale','soc.religion.christian']

for cate in cate_list:
    category = [cate]
    x_train = fetch_20newsgroups(subset='all', categories=category, shuffle=True, random_state=42, remove=('headers','footers','quotes'))
    TFIDF = TfidfVectorizer(analyzer='word',tokenizer=tk, max_features=10, stop_words=text.ENGLISH_STOP_WORDS)
    x_train_tfidf= TFIDF.fit_transform(x_train.data)
    print 'in '+cate+'category, the top 10 words are:'
    print TFIDF.vocabulary_.keys()
    print '\n'
