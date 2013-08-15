TEST_RUNNER = 'mocking_django.unit_test_runner.NoDbTestRunner'

ROOT_URLCONF = 'mocking_django.urls'

SECRET_KEY = 'abcd'

DATABASES = {}

# Don't do this if you're a purist about FS access in your unit tests
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

INSTALLED_APPS = (
    'library',
)
