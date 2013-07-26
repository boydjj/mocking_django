from django.shortcuts import render_to_response
from django.template import RequestContext
from library.forms import BookForm
from library.models import Book


def add_book(request):
    if request.method == 'GET':
        form = BookForm()
        return render_to_response('library/add_book.html', RequestContext(request, {'form': form}))
    elif request.method == 'POST':
        f = BookForm(request.POST)
        new_book = f.save()
        return render_to_response('library/added_book.html', {'book': new_book})

def book_detail(request, book_id):
    return render_to_response('library/book_detail.html', {'book': Book.objects.get(pk=book_id)})
