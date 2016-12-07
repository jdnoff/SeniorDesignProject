from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View
from .forms import TopicSearchForm
from .forms import AuthorSearchForm
from .forms import AuthorSearchSubsetForm
from topic_search import do_topic_search
from author_search import get_author_papers
from author_search import search_papers, get_papers_by_id


class AboutUsView(TemplateView):
	template_name = 'about_us.html'


class TopicSearchView(View):
	form_class = TopicSearchForm
	template_name = 'search.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {
			'form': form,
			'blurb': 'Enter information about the manuscript you would like to find reviewers for'
		})

	def post(self, request, *args, **kwargs):
		"""
		Handles a POST request and renders a results page. Unless the form is invalid then it is redisplayed
		:param request: POST request
		:param args:
		:param kwargs:
		:return:
		"""
		form = self.form_class(request.POST)
		if form.is_valid():
			# <process form cleaned data>
			data = form.cleaned_data
			title = data['manuscript_title']
			abstract = data['manuscript_abstract'].lower()

			author_list = do_topic_search(abstract)

			return render(request, 'results.html', {
				'results_list': author_list,
				'query': [title],
				'max_citations': max([author.citations for author in author_list], default=1000)
			})

		return render(request, self.template_name, {
			'form': form,
			'blurb': 'Enter information about the manuscript you would like to find reviewers for'
		})


class AuthorSearchView(View):
	form_class = AuthorSearchForm
	template_name = 'subset_page.html'
	search_tmp = 'search.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.search_tmp, {
			'form': form,
			'blurb': 'Enter the name of the author you would like to review'
		})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)

		# Search subset of papers
		if 'subset' in request.POST:
			paperIds = request.POST.getlist('paper_list')
			papers = get_papers_by_id(paperIds)
			author_list = search_papers(papers)

			return render(request, 'results.html', {
				'results_list': author_list,
				'query': [p.title for p in papers],
				'max_citations': max([author.citations for author in author_list], default=1000)
			})
		else:
			# get author name and body of work
			if form.is_valid():
				# <process form cleaned data>
				data = form.cleaned_data
				author = data['author'].lower()
				papers = get_author_papers(author)
				subsetForm = AuthorSearchSubsetForm()
				c = [(p.id, p.title) for p in papers]
				subsetForm.fields['paper_list'].choices = c
				return render(request, self.template_name, {'form': subsetForm})

		return render(request, self.search_tmp, {
			'form': form,
			'blurb': 'Enter the name of the author you would like to review'
		})
