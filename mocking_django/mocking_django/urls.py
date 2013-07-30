from django.conf.urls import patterns, url

from django.views.generic import TemplateView, ListView

from library import models as library_models
from library.views.authors import AddAuthorView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='library/index.html'), name='index'),

    # Books views - let's keep these functional as much as possible
    url(r'^books/$', ListView.as_view(template_name='library/book_list.html', model=library_models.Book), name='library.views.books.book_index'),
    url(r'^books/(\d+)/$', 'library.views.books.book_detail', name='library.views.books.book_detail'),
    url(r'^books/add/$', 'library.views.books.add_book', name='library.views.books.add_book'),

    # Authors views - let's keep these class-based
    url(r'^authors/$', ListView.as_view(template_name='library/author_list.html', model=library_models.Author), name='library.views.authors.author_index'),
    url(r'^authors/add/$', AddAuthorView.as_view(), name='library.views.authors.add_author')

)
