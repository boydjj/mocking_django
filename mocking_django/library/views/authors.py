from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View
from library.models import Author


class AddAuthorView(View):
    def get(self, request):
        return render_to_response('library/add_author.html', RequestContext(request))

    def post(self, request):
        name = request.POST['author_name']

        author = Author.objects.create(name=name)

        return render_to_response('library/added_author.html', RequestContext(request, {'author': author}))
