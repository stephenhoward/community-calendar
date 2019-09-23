import unittest
from event_calendar.site_settings import site_settings, LanguageException

class TestSiteSettings(unittest.TestCase):

    def test_default_language(self):
        assert( site_settings.default_language == 'en' )
        site_settings.default_language = 'es'
        assert( site_settings.default_language == 'es' )
        assert( site_settings._settings['default_language'] == 'es' )

        with self.assertRaises(LanguageException):
            site_settings.default_language = 'not_a_lang'

    def test_languages_available(self):
        assert( isinstance( site_settings.languages, list ) )
        with self.assertRaises(LanguageException):
            site_settings.languages = ['en','boo']

        site_settings.languages = ['en','es','fr','zh']

        assert( 'fr' in site_settings._settings['languages'] )

    def test_bad_key(self):
        site_settings.test_me = 'bad';
        assert( 'test_me' not in site_settings._settings );

    def test_info(self):
        assert( isinstance( site_settings.info('en'), dict ) )
        with self.assertRaises( Exception ):
            site_settings.set_info('en',{ 'key': 'value' } )

        with self.assertRaises( Exception ):
            site_settings.set_info('en',{'site_title':['bad','type']} )

        site_settings.set_info('en',{'site_title':'nonsense'})
        assert( site_settings._settings['info']['en']['site_title'] == 'nonsense' )

if __name__ == '__main__':
    unittest.main()
