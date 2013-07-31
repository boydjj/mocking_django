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
To run the standard Django tests for the `library` app, do the usual:

    $ pwd
    /path/to/this/repository
    $ python mocking_django/manage.py test library

To run the pytest- and mock-based unit tests for the same app, do this:

    $ pwd
    /path/to/this/repository
    $ DJANGO_SETTINGS_MODULE=mocking_django.settings_test_unit py.test mocking_django/library/
