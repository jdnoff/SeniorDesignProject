# Author object file
from AS_RequestHandler import test_query
from AS_RequestHandler import query

class Author:
    # List of Class Attributes
    # paperTitles -- list of all papers associated with this author given by the query (given by 'Ti' attribute)
    # keyWords -- list of all keywords from all papers in paperTitles (given by 'W' attribute)
    # fieldsOfStudy -- list of all fields of study the papers encompass (given by 'F.FN' attribute)
    # citationByPaper -- number of citations for each paper in result list (given by 'CC' attribute)


    def __init__(self):
        # results = query()
        results = test_query()

        self.paperTitles = []
        self.keyWords = []
        self.fieldsOfStudy = []
        self.citationByPaper = []
        for result in results:
            self.paperTitles.append(result['Ti'].title())

        print(self.paperTitles)


