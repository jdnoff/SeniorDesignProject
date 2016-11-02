"""
	This contains the constants needed to make requests to the academic servies api
"""

# Subscription key placed in header
REQUEST_HEADER = {'Ocp-Apim-Subscription-Key': '5569c93188b746fcab48355fa04a68f8'}

# REST endpoints
EVALUATE_URL = 'https://api.projectoxford.ai/academic/v1.0/evaluate'
INTERPRET_URL = 'https://api.projectoxford.ai/academic/v1.0/interpret'
HIST_URL = 'https://api.projectoxford.ai/academic/v1.0/calchistogram'

# Calchistogram and Evaluate request parameters
PARAM_EXPR = 'expr'
PARAM_MODEL = 'model'
PARAM_COUNT = 'count'
PARAM_ORDERBY = 'orderby'
PARAM_ATTRIBUTES = 'attributes'
PARAM_OFFSET = 'offset'

# Interpret request parameters
PARAM_QUERY = 'query'
PARAM_COMPLETE = 'complete'
PARAM_TIMEOUT = 'timeout'

# Entity attributes
ATT_ID = 'Id'  # Entity ID
ATT_PAPER_TITLE = 'Ti'  # Paper title
ATT_YEAR = 'Y'  # Paper year
ATT_DATE = 'D'  # Paper date
ATT_CITATIONS = 'CC'  # Citation count
ATT_EST_CITATIONS = 'ECC'  # Estimated citation Count
ATT_AUTHOR_NAME = 'AA.AuN'  # Author name
ATT_AUTHOR_ID = 'AA.AuId'  # Author ID
ATT_AUTHOR_AFFILIATION = 'AA.AfN'  # Author affiliation name
ATT_AUTHOR_AFFILIATION_ID = 'AA.AfId'  # Author affiliation ID
ATT_FIELD_OF_STUDY = 'F.FN'  # Field of study name
ATT_FIELD_OF_STUDY_ID = 'F.FId'  # Field of study ID
ATT_JOURNAL_NAME = 'J.JN'  # Journal name
ATT_JOURNAL_ID = 'J.JId'  # Journal ID
ATT_CONFERENCE_NAME = 'C.CN'  # Conference series name
ATT_CONFERENCE_ID = 'C.CId'  # Conference series ID
ATT_WORDS = 'W' # Words from paper title/abstract for full text search
ATT_EXTENDED = 'E'  # Extended metadata (see table below)

ATT_EXT_DISPLAY_NAME = 'DN'  # Display Name of the paper
ATT_EXT_DESCRIPTION = 'D'  # Description
ATT_EXT_SOURCES = 'S'  # Sources - list of web sources of the paper, sorted by static rank
ATT_EXT_SOURCE_TYPE = 'S.Ty'  # Source Type (1:HTML, 2:Text, 3:PDF, 4:DOC, 5:PPT, 6:XLS, 7:PS)
ATT_EXT_SOURCE_URL = 'S.U'  # Source URL
ATT_EXT_VENUE_NAME_FULL = 'VFN'  # Venue Full Name - full name of the Journal or Conference
ATT_EXT_VENUE_NAME_SHORT = 'VSN'  # Venue Short Name - short name of the Journal or Conference
ATT_EXT_VOLUME = 'V'  # Volume - journal volume
ATT_EXT_ISSUE = 'I'  # Issue - journal issue
ATT_EXT_FIRST_PAGE = 'FP'  # FirstPage - first page of paper
ATT_EXT_LAST_PAGE = 'LP'  # LastPage - last page of paper
ATT_EXT_DOI = 'DOI'  # Digital Object Identifier
