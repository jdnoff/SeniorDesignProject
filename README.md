# README #

# Expert Finder Tool #
Streamlining the peer review process

## What is Expert Finder? ##
Expert Finder is a web-accessible tool designed to aid academic 
professionals in the peer review process by querying scholarly libraries 
to compile a list of experts for a specific topic.

## Use Cases ##
### Topic Search ###
Topic Search is designed to help the peer review process for a single academic manuscript. Enter a manuscript's abstract and title to recieve a list of academic professionals that have similar fields of research, ranking them based on how similar thier work is to the manuscript. 
* Rank potential reviewers based on number of papers written on the searched subject,
    the number of times their papers have been cited,
    and the time since the reviewer has published a paper related to the topic

###  Author Search ###
Author search allows the user to find potential reviewers for an already established author. The user queries the authors name, from there the user is allowed to select a subset of the authors papers. After doing so, a list of ranked reviewers is returned to the user. Each ranked based on their ability to review the author's body of work.


## Technical Information ##
### Web Framework ###
ExpertFinder is powered by the Django Web framework

### Academic Data ###
ExpertFinder uses the academic databases of Microsoft Academic to provide its service. Microsoft's Academic Knowledge API provides access to its academic databases through the REST API. 

### Memcached ###
ExpertFinder takes advantage of memcached's caching service and uses it to cache the results that it retrieves from Microsoft Academic. Doing so allows ExpertFinder to reduce the overall number of calls it must make to the database and allows it to provide a faster service.

### Required Packages ###
* Django==1.10.1
* nltk==3.2.1
* python-memcached==1.58
* requests==2.11.1
* six==1.10.0


### Installation ###
#### Installation on ubuntu 16.04 ####
* Install required packages 
    * python3
    * django
    * memcached
    * gunicorn
* Clone repo
* 

## Useful Links ##

### Django ###
* https://docs.djangoproject.com/en/1.10/intro/tutorial01/
* https://docs.djangoproject.com/en/1.10/
* https://docs.djangoproject.com/en/1.10/intro/overview/

### Microsoft Academic ###
* https://www.microsoft.com/cognitive-services/en-us/Academic-Knowledge-API/documentation/EvaluateMethod
* https://www.microsoft.com/cognitive-services/en-us/Academic-Knowledge-API/documentation/InterpretMethod
* https://www.microsoft.com/cognitive-services/en-us/Academic-Knowledge-API/documentation/QueryExpressionSyntax
* https://dev.projectoxford.ai/docs/services/56332331778daf02acc0a50b/operations/565d753be597ed16ac3ffc03
* https://dev.projectoxford.ai/docs/services/56332331778daf02acc0a50b/operations/56332331778daf06340c9666/console