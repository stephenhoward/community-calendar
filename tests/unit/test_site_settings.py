import unittest
from event_calendar.site_settings import site_settings, LanguageException

class TestSiteSettings(unittest.TestCase):

    def test_lang(self):
        assert( site_settings.default_language == 'en' )
        site_settings.default_language = 'es'
        assert( site_settings.default_language == 'es' )
        assert( site_settings._settings['default_language'] == 'es' )

        with self.assertRaises(LanguageException):
            site_settings.default_language = 'not_a_lang'

if __name__ == '__main__':
    unittest.main()
