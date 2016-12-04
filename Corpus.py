# This is an object file for the Corpus object
# which will be generated for each query.
# It will contain the words in the abstracts
# of each paper considered in the query
# and their IDF scores

from similarity_measure import tf_idf
from textblob import TextBlob
from nltk.corpus import stopwords

class Corpus:
    def __init__(self, docList):
        documents = []
        for doc in docList:
            documents.append(Document(doc, docList))

class Document:
    def __init__(self, doc, docList):
        self.text = doc
        self.words = []
        cachedStopWords = stopwords.words("english")
        for word in doc.words:
            if word not in cachedStopWords:
                tfidf = tf_idf(word, doc, docList)
                self.words.append(AbWord(word, tfidf))
                print(word, tfidf)

class AbWord:
    def __init__(self, word, tfidf):
        self.word = word
        self.tfidf = tfidf