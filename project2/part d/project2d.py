from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re
import nltk 
import string
from nltk.stem.snowball import SnowballStemmer



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

categories = ['comp.graphics','comp.os.ms-windows.misc','comp.sys.ibm.pc.hardware','comp.sys.mac.hardware','rec.autos','rec.motorcycles','rec.sport.baseball','rec.sport.hockey']
twenty_train = fetch_20newsgroups(subset='train', shuffle=True, random_state=42)
twenty_test = fetch_20newsgroups(subset='test', shuffle=True, random_state=42)

TFIDF = TfidfVectorizer(analyzer='word',tokenizer=tk, stop_words=text.ENGLISH_STOP_WORDS)
x_train_tfidf= TFIDF.fit_transform(twenty_train.data)
x_test_tfidf=TFIDF.fit_transform(twenty_test.data)


from sklearn.decomposition import TruncatedSVD
SVD = TruncatedSVD(n_components=50, algorithm='arpack')

LSI_X_train = SVD.fit_transform(x_train_tfidf)
LSI_X_test=SVD.fit_transform(x_test_tfidf)
print 'the SVD train matrix dimension is \n'
print LSI_X_train.shape
print '\n'
print 'the SVD test matrix dimension is \n'
print LSI_X_test.shape
