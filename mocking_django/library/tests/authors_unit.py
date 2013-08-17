from mock import patch

from django.test import SimpleTestCase, RequestFactory

from library.views.authors import AddAuthorView
from library.tests.utils import render_to_response_echo

__all__ = ['AddAuthorUnitTestCase', 'AddAuthorUnitTestCaseWithManualPatching']


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

        with patch('library.views.authors.render_to_response') as mock_render_to_response:
            with patch('library.views.authors.RequestContext') as mock_request_context:
                with patch('library.views.authors.Author.objects.create') as mock_author_create:
                    response = view(request)

        # Verify that we created our Author
        mock_author_create.assert_called_with(name=request.POST['author_name'])

        # Verify that we called render_to_response properly
        mock_request_context.assert_called_with(request,
                                                {'author': mock_author_create.return_value})
        mock_render_to_response.assert_called_with('library/added_author.html',
                                                   mock_request_context.return_value)

class AddAuthorUnitTestCaseWithManualPatching(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        cls.rf = RequestFactory()
        cls.add_author_url = '/fake/path/to/authors/add/'

    def setUp(self):
        self.render_to_response_patcher = \
            patch('library.views.authors.render_to_response', render_to_response_echo)
        self.request_context_patcher = patch('library.views.authors.RequestContext')
        self.author_create_patcher = patch('library.views.authors.Author.objects.create')

        self.render_to_response_patcher.start()
        self.mock_request_context = self.request_context_patcher.start()
        self.mock_author_create = self.author_create_patcher.start()

    def tearDown(self):
        self.render_to_response_patcher.stop()
        self.request_context_patcher.stop()
        self.author_create_patcher.stop()

    def test_post_happy_path(self):
        """
        Patch all the dependencies of AddAuthorView.post and then assert things
        about those dependencies
        """
        request = self.rf.post(self.add_author_url,
                               data={'author_name': 'Never Before Seen Author'})
        view = AddAuthorView.as_view()

        response = view(request)

        assert response['template_name'] == 'library/added_author.html'
        self.mock_author_create.assert_called_with(name=request.POST['author_name'])
        self.mock_request_context.assert_called_with(request,
                                                     {'author': self.mock_author_create.return_value})
