from django.http import HttpResponse, Http404
from django.test import RequestFactory
import pytest
from library.views.books import book_detail

from mock import patch, Mock
from library.models import Book


class TestBookDetail(object):
    """
    Test all the same portions of our book_detail view as the functional tests,
    but without DB access.
    """
    def setup_method(self, method):
        # Django's RequestFactory builds requests we can just pass into views
        self.rf = RequestFactory()

        # Please note that these are *totally* unnecessary for the functionality
        # of our view, since we'll be patching all the relevant helpers anyway.
        # However, RequestFactory's .get() method requires a URL.
        self.valid_book_url = '/fake/url/to/prove/a/point/'
        self.invalid_book_url = '/another/fake/url/that/has/no/id/'

    def test_detail_view_returns_ok(self):
        """
        Validate that in the usual case (where there is a Book corresponding
        to the passed-in ID) we get a 200 and that we call all the relevant
        helpers correctly.
        """
        request = self.rf.get(self.valid_book_url)

        # Patch the get_object_or_404 helper
        with patch('library.views.books.get_object_or_404') as mock_get_object_or_404:
            # Now patch the render_to_response helper
            with patch('library.views.books.render_to_response') as mock_render_to_response:
                # Now set the patched render_to_response to return a valid response
                mocked_response = HttpResponse()
                mocked_response.status_code = 200
                mock_render_to_response.return_value = mocked_response

                # Now, actually get the response from book_detail
                response = book_detail(request, 1)

        # Let's make sure we got a 200 and that we used the right template
        assert response.status_code == 200
        mock_render_to_response.assert_called_with('library/book_detail.html', {'book': mock_get_object_or_404.return_value})

        # Let's validate that get_object_or_404 was called with the right args
        mock_get_object_or_404.assert_called_with(Book, id=1)

    def test_detail_response_includes_title(self):
        """
        Validate that our template renders book details correctly.

        N.B.: I don't actually recommend doing this with true unit tests because
        it relies on filesystem access. It is included here only for parity.
        Note the settings in settings_test_unit.py marked "BAD FOR UNIT TESTS".
        """
        request = self.rf.get(self.valid_book_url)

        # Patch the get_object_or_404 helper
        with patch('library.views.books.get_object_or_404') as mock_get_object_or_404:
            # Set it to return an object that looks like a Book with authors
            fake_book = Mock()
            fake_book.title = 'The Left Hand of Darkness'
            fake_book.authors = ['Ursula K. Le Guin']
            fake_book.__unicode__ = lambda x: fake_book.title
            mock_get_object_or_404.return_value = fake_book

            # Now call book_detail and get its response
            response = book_detail(request, 1)

        expected = '<h1>Detail for The Left Hand of Darkness</h1>'

        assert expected in response.content

    def test_detail_returns_404_for_nonexistent_book(self):
        """
        Validate that book_detail returns a 404 when there's no such Book.
        """
        request = self.rf.get(self.invalid_book_url)

        # Patch the get_object_or_404 helper
        with patch('library.views.books.get_object_or_404') as mock_get_object_or_404:
            # This time, let's make it raise a 404 since that's what the real
            # get_object_or_404 does if it can't find the object.
            mock_get_object_or_404.side_effect = Http404('No Book matches the given query.')

            # Now call book_detail and confirm we got a 404 exception
            with pytest.raises(Http404):
                book_detail(request, 1)
