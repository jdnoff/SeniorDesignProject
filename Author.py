# Author object file
from AS_RequestHandler import test_query

class Author:
    # List of Class Attributes
    # paperTitles -- list of all papers associated with this author given by the query (given by 'Ti' attribute)
    # keyWords -- list of all keywords from all papers in paperTitles (given by 'W' attribute)
    # fieldsOfStudy -- list of all fields of study the papers encompass (given by 'F.FN' attribute)
    # citationByPaper -- number of citations for each paper in result list (given by 'CC' attribute)
        # used to sum all total citations for an author

    def __init__(self, input):
        # input should be the json result of a query for an author
        # which gets the attributes 'Ti', 'W', 'F.FN', 'CC'
        results = input
        # results = test_query()

        self.paperTitles = []
        self.keyWords = []
        self.fieldsOfStudy = []
        self.citationByPaper = []
        for result in results:
            self.paperTitles.append(result['Ti'].title())
            self.keyWords.append(result['W'])
            self.fieldsOfStudy.append(result['F.FN'].title())
            self.citationByPaper.append(result['CC'])
        self.totalCitations = self.sumCitations()

    def sumCitations(self):
        total = 0
        for i in self.citationByPaper:
            total += self.citationByPaper[i]
        return total



