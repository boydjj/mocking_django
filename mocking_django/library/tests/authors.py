from django.test import TestCase
from library.models import Author

__all__ = ['AddAuthorTestCase']


class AddAuthorTestCase(TestCase):
    def test_get_returns_correct_template(self):
        response = self.client.get('/authors/add/')
        self.assertIn('library/add_author.html', [t.name for t in response.templates])
        expected = '<input type="text" id="author_name_input" name="author_name">'
        self.assertInHTML(expected, response.content)

    def test_post_happy_path(self):
        response = self.client.post('/authors/add/', {'author_name': 'Never Before Seen Author'})

        # Sanity check; let's make sure we got the right template
        self.assertIn('library/added_author.html', [t.name for t in response.templates])

        # Now let's check and make sure there's an author with this name
        Author.objects.get(name='Never Before Seen Author')
