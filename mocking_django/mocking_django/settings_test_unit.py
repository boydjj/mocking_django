TEST_RUNNER = 'mocking_django.unit_test_runner.NoDbTestRunner'

ROOT_URLCONF = 'mocking_django.urls'

SECRET_KEY = 'abcd'

DATABASES = {}

# BAD FOR UNIT TESTS - requires filesystem access
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

INSTALLED_APPS = (
    'library',
)
