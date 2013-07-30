from django.test import TestCase
from library.forms import BookForm
from library.models import Author, Book

__all__ = ['BookDetailTestCase', 'AddBookTestCase']


class BookDetailTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Ursula K. Le Guin')
        self.book = Book.objects.create(title='The Left Hand of Darkness', page_length=304)
        self.book.authors.add(self.author)

        self.valid_book_url = '/books/{0}/'.format(self.book.id)
        self.invalid_book_url = '/books/{0}/'.format(self.book.id+1)

    def test_detail_view_returns_ok(self):
        response = self.client.get(self.valid_book_url)
        self.assertEqual(response.status_code, 200)

    def test_detail_response_includes_title(self):
        response = self.client.get(self.valid_book_url)
        expected = '<h1>Detail for The Left Hand of Darkness</h1>'
        self.assertInHTML(expected, response.content)

    def test_detail_returns_404_for_nonexistent_book(self):
        response = self.client.get(self.invalid_book_url)
        self.assertEqual(response.status_code, 404)


class AddBookTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name='Ursula K. Le Guin')
        self.author2 = Author.objects.create(name='Neal Stephenson')

    def test_get_returns_correct_template(self):
        response = self.client.get('/books/add/')
        self.assertIn('library/add_book.html', [t.name for t in response.templates])
        self.assertIsInstance(response.context['form'], BookForm)

    def test_post_happy_path(self):
        response = self.client.post('/books/add/', {'title': 'The Left Hand of Darkness', 'page_length': 304, 'authors': [self.author1.id, self.author2.id]})
        expected = '<h1>Book added</h1>'
        self.assertInHTML(expected, response.content)

    def test_post_invalid_author_raises_ValueError(self):
        args = '/books/add/', {'title': 'The Left Hand of Darkness', 'page_length': 304, 'authors': [self.author2.id+1]}
        self.assertRaises(ValueError, self.client.post, *args)

    def test_post_non_string_page_length_raises_ValueError(self):
        args = '/books/add/', {'title': 'The Left Hand of Darkness', 'page_length': 'abcd', 'authors': [self.author2.id]}
        self.assertRaises(ValueError, self.client.post, *args)
