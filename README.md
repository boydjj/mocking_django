mocking-django
==============

This is a demo app used for Jeremy Boyd's "Mocking Django" talk. It will be a
simple 'personal library' application that will demonstrate unusual testing
techniques for Django applications.

Running the tests
-----------------
To run the standard Django tests for the `library` app, do the usual:

    $ python manage.py test library

To run the pytest- and mock-based unit tests for the same app, do this:

    $ DJANGO_SETTINGS_MODULE=mocking_django.settings_test_unit py.test mocking_django/library/
