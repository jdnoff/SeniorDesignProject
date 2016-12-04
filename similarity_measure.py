# file which contains all functions for measuring
# similarity between documents

import math
import numpy as np

def term_freq(word, doc):
	return doc.words.count(word)/len(doc.words)

def n_containing(word, docList):
	return sum(1 for doc in docList if word in doc.words)

def inverse_doc_freq(word, docList):
	return math.log(len(docList) / (1+n_containing(word, docList)))

def tf_idf(word, doc, docList):
	return term_freq(word, doc) * inverse_doc_freq(word, docList)

def keySplit(doc, cachedStopWords):
	wordList = []
	for term in doc:
		list = term.split(" ")
		for word in list:
			if word not in cachedStopWords:
				wordList.append(word)
	return wordList

def jaccard_test(doc_one, doc_two):
	union = set(doc_one).union(doc_two)
	intersect = set(doc_one).intersection(doc_two)
	index = len(intersect) / len(union)
	return index

def cosine_sim(query, document):
	dotProduct = np.dot(query, document)
	magQ = np.linalg.norm(query)
	magD =np.linalg.norm(document)
	if magD == 0:
		return 0
	sim = (dotProduct) / (magQ * magD)
	return sim
