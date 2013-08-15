from mock import patch

from django.test import SimpleTestCase, RequestFactory

from library.views.authors import AddAuthorView
from library.tests.utils import render_to_response_echo

__all__ = ['AddAuthorUnitTestCase']


class AddAuthorUnitTestCase(SimpleTestCase):
    """
    Test all the same portions of our AddAuthorView as the functional tests, but
    without DB access.
    """
    @classmethod
    def setUpClass(cls):
        cls.rf = RequestFactory()
        cls.add_author_url = '/fake/path/to/authors/add/'

    def test_get_returns_correct_template(self):
        """
        Demonstrates patching a dependency of our AddAuthorView.get method with
        render_to_response_echo from above.
        """
        request = self.rf.get(self.add_author_url)
        view = AddAuthorView.as_view()

        with patch('library.views.authors.render_to_response', render_to_response_echo):
            response = view(request)

        assert response['template_name'] == 'library/add_author.html'

    def test_post_happy_path(self):
        """
        Patch all the dependencies of AddAuthorView.post and then assert things
        about those dependencies
        """
        request = self.rf.post(self.add_author_url, data={'author_name': 'Never Before Seen Author'})
        view = AddAuthorView.as_view()

        with patch('library.views.authors.render_to_response', render_to_response_echo):
            with patch('library.views.authors.RequestContext') as mock_request_context:
                with patch('library.views.authors.Author.objects.create') as mock_author_create:
                    response = view(request)

        assert response['template_name'] == 'library/added_author.html'
        mock_author_create.assert_called_with(name=request.POST['author_name'])
        mock_request_context.assert_called_with(request, {'author': mock_author_create.return_value})
