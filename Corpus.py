
from similarity_measure import tf_idf

class Corpus:
    """
    List of Class Attributes:
    documents -- A dict of all the documents returned by requests to Microsoft Academic.
    words -- A list of all non-stopword words in the input query.
    scoredDocs -- list of Document objects generated from the documents attribute.
    vectors -- list of the vector attribute for each document in scoredDocs
    """
    def __init__(self, docList, wordList):
        """
        Constructs the initial corpus object. The words attribute is set equal to wordList
        and the documents attribute is set equal to docList. scoredDocs and vectors are
        initialized as blank lists.
        :param: docList: A dict of all the documents returned by requests to Microsoft Academic.
                wordList: A list of all non-stopword words in the input query.
        :return: No return value
        """
        self.documents = docList  # now a dict
        self.words = wordList
        self.scoredDocs = []
        self.vectors = []

    def constructVectors(self):
        """
        A Document object is created for each document pulled from the query. Then,
        for each Document object, a TF-IDF vector is constructed from the TF-IDF scores
        of the corpus words present in each document. The computed vector is then stored in the
        vectors attribute.
        :param: No parameters. Uses the self.documents attribute
                to obtain list of all documents in the query.
        :return: No return value
        """
        for docId in self.documents.keys():
            self.scoredDocs.append(Document(self.documents[docId], self.documents.values(), self.words, docId))
        for doc in self.scoredDocs:
            self.vectors.append(doc.constructIDFVector())

class Document:
    """
    List of Class Attributes:
    id -- The ID number of the document.
    text -- The full text of the document's abstract.
    words -- A list of AbWord objects created for each of the non-stopword words
             in the user's input query. The AbWord object contains a word's TF-IDF score
             with respect to this document.
    score -- The Cosine Similarity score assigned to the document based on its
             similarity to the user's query.
    vector -- A vector composed of the TF-IDF scores pulled from each AbWord object stored in the
              words attribute.
    """
    def __init__(self, doc, docList, wordList, id):
        """
        Constructs a Document object. Stores doc and id parameters as the text and id
        attributes respectively. Then, the TF-IDF score of each word in the corpus is calculated
        with respect to this document and stored in the words attribute as an AbWord object.
        :param: doc: The full text of the document's abstract.
                id: The ID number of the document.
                docList: A dict of all the documents returned by requests to Microsoft Academic.
                wordList: A list of all non-stopword words in the input query.
        :return: No return value
        """
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
        """
        Constructs a TF-IDF vector from a document by iterating through each AbWord object
        in the words attribute, pullinf the tf-idf score of the word and appending it to the
        vector attribute. Stores this vector as an attribute of the document.
        :param: No parameters. Uses self.words attribute.
        :return: No return value
        """
        for word in self.words:
            self.vector.append(word.tfidf)
        return self.vector

    def getWords(self):
        """
        returns a list of the word attribute of all AbWords in self.words
        for string comparison purposes.
        :param: No parameters. Uses self.words attribute.
        :return: getWords: a list of the text of each word in the document
        """
        getWords = []
        for word in self.words:
            getWords.append(word.word)
        return getWords

    def addScore(self, score):
        """
        Stores a given similarity score as an attribute of the document.
        :param: score: a Cosine Similarity score calculated for the document.
        :return: No return value.
        """
        self.score = score

class AbWord:
    """
    List of Class Attributes:
    word -- string containing the text of the word
    tfidf -- the TF-IDF score of the word with respect to the
             document which contains this object
    """
    def __init__(self, word, tfidf):
        """
        Constructs an AbWord object by storing the given text and tfidf score.
        :param: tfidf: the TF-IDF score of the word with respect to the
                       document which contains this object
                word: string containing the text of the word
        :return: No return value.
        """
        self.word = word
        self.tfidf = tfidf

    def getWord(self):
        """
        Returns the text of the word. Used for string comparison.
        :param: No parameters. uses self.word attribute.
        :return: No return value.
        """
        return self.word