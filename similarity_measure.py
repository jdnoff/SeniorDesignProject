# file which contains all functions for measuring
# similarity between documents

import math
import numpy as np

# TF-IDF functions based on examples from:
#		http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/ '
#
def term_freq(word, doc):
	"""
	Calculates the Term Frequency of a given word in a given document.
	:param: word: string containing text of a word.
			doc: full text of the abstract of a document.
	:return: Returns the Term Frequency value.
	"""
	return doc.words.count(word)/len(doc.words)

def n_containing(word, docList):
	"""
	Given a list of documents, Calculates the number of documents a specific word appears in.
	:param: word: string containing text of a word.
			docList: list of all the abstracts of documents in the corpus.
	:return: Returns the number of documents the word appears in.
	"""
	return sum(1 for doc in docList if word in doc.words)

def inverse_doc_freq(word, docList):
	"""
	Given a list of documents, Calculates the Inverse Document Frequency of a specific word.
	:param: word: string containing text of a word.
			docList: list of all the abstracts of documents in the corpus.
	:return: Returns the Inverse Document Frequency value.
	"""
	return math.log(len(docList) / (1+n_containing(word, docList)))

def tf_idf(word, doc, docList):
	"""
	Given a list of documents, Calculates the Term Frequence * Inverse Document Frequency
	value of a specific word with respect to a specific document.
	:param: word: string containing text of a word.
			docList: list of all the abstracts of documents in the corpus.
	:return: Returns the TF-IDF value.
	"""
	return term_freq(word, doc) * inverse_doc_freq(word, docList)

def keySplit(doc, cachedStopWords):
	"""
	Splits a string of a document's abstract into a list of words, removing all stopwords.
	:param: doc: The text of a document's abstract
			cachedStopWords: list of all stopwords.
	:return: wordList: A list of all non-stopword words in a document's abstract.
	"""
	wordList = []
	for term in doc:
		list = term.split(" ")
		for word in list:
			if word not in cachedStopWords:
				wordList.append(word)
	return wordList

def cosine_sim(query, document):
	"""
	Given two TF-IDF vectors, calculates the Cosine similarity of a document with respect to
	the query. Returns 0 if the document contains none of the words in the query.
	:param: query: TF-IDF vector for the user's query.
			document: TF-IDF vector for the document being compared.
	:return: sim: Cosine Similarity value of the document compared to the query.
	"""
	dotProduct = np.dot(query, document)
	magQ = np.linalg.norm(query)
	magD =np.linalg.norm(document)
	if magD == 0:
		return 0
	sim = (dotProduct) / (magQ * magD)
	return sim
