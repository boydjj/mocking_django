mocking-django
==============
This is a demo app used for Jeremy Boyd's "Mocking Django" talk. It will be a simple 'personal library' application that will demonstrate unusual testing techniques for Django applications.

Setting up the application
--------------------------
You should be able to run this application with relative ease using `virtualenv` and `virtualenvwrapper`:

    $ mkvirtualenv mocking-django
    ...
    $ cd /path/to/this/repository
    $ pip install -r build/pip-requirements.txt
    $ python mocking_django/manage.py syncdb
    ...
    $ python mocking_django/manage.py runserver
    Validating models...

    0 errors found
    July 30, 2013 - 19:39:49
    Django version 1.5.1, using settings 'mocking_django.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.


Running the tests
-----------------
To run all tests for the `library` app, do the usual:

    $ pwd
    /path/to/this/repository/mocking_django
    $ python manage.py test library

To run only the 'traditional' Django tests, you'll have to select them individually:

    $ pwd
    /path/to/this/repository/mocking_django
    $ python manage.py test library.BookDetailTestCase library.AddBookTestCase

To run the mock-based tests that don't ever access the DB, you'll need to select them similarly:

    $ pwd
    /path/to/this/repository/mocking_django
    $ python manage.py test library.BookDetailUnitTestCase library.AddBookUnitTestCase --settings=mocking_django.settings_test_unit

Note the addition of the `--settings` flag. `settings_test_unit.py` changes the test runner so it doesn't do anything with the DB and defines some (relatively) innocuous settings. You can always run the 'true' unit tests without this flag, but I prefer to run with settings specific to unit tests that prove to me that nothing is accessing any external resources.
