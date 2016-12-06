# This is an object file for the Corpus object
# which will be generated for each query.
# It will contain the words in the abstracts
# of each paper considered in the query
# and their IDF scores

from similarity_measure import tf_idf
from textblob import TextBlob
from nltk.corpus import stopwords

class Corpus:
    def __init__(self, docList, wordList):
        self.documents = docList  # now a dict
        self.words = wordList
        self.scoredDocs = []
        self.vectors = []

    def constructVectors(self):
        for docId in self.documents.keys():
            self.scoredDocs.append(Document(self.documents[docId], self.documents.values(), self.words, docId))
        for doc in self.scoredDocs:
            self.vectors.append(doc.constructIDFVector())

class Document:
    def __init__(self, doc, docList, wordList, id):
        self.id = id
        self.text = doc
        self.words = []
        self.score = 0
        self.vector = []
        for word in wordList:
            tfidf = 0
            if word in doc.words:
                tfidf = tf_idf(word, doc, docList)
            self.words.append(AbWord(word, tfidf))

    def constructIDFVector(self):
        for word in self.words:
            self.vector.append(word.tfidf)
        return self.vector

    def getWords(self):
        getWords = []
        for word in self.words:
            getWords.append(word.word)
        return getWords

    def addScore(self, score):
        self.score = score

    def createVector(self):
        attributes = []
        for word in self.words:
            attributes.append(word.tfidf)
        return attributes

class AbWord:
    def __init__(self, word, tfidf):
        self.word = word
        self.tfidf = tfidf

    def getWord(self):
        return self.word