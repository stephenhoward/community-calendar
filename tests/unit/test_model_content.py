import unittest
import event_calendar.model.content

class TestCodes(unittest.TestCase):

    def test_codes_exist(self):
        assert( 'en' in event_calendar.model.content.LanguageCode.__members__ )
        assert( 'es' in event_calendar.model.content.LanguageCode.__members__ )
        assert( 'fr' in event_calendar.model.content.LanguageCode.__members__ )


if __name__ == '__main__':
    unittest.main()