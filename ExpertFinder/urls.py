"""ExpertFinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from ExpertFinderTool import views
from ExpertFinderTool.views import LandingView
from ExpertFinderTool.views import TopicSearchView
from ExpertFinderTool.views import AuthorSearchView
from ExpertFinderTool.views import ResultsView

urlpatterns = [
	url(r'^results/', ResultsView.as_view(), name='results'),
	url(r'^author/', AuthorSearchView.as_view(), name='author_search'),
	url(r'^topic/', TopicSearchView.as_view(), name='topic_search'),
	url(r'^', LandingView.as_view(), name='home'),
	url(r'^admin/', admin.site.urls),
]
