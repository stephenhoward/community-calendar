import unittest
from event_calendar.config import config

class TestConfig(unittest.TestCase):

    def test_get(self):
        assert( isinstance(config._config,dict) )
        assert( config.get('db') != None )
        assert( config.get('db','host') == 'postgres' )
        self.assertRaises( Exception, config.get, 'not_a_key' )

    def test_set(self):
        self.assertRaises( Exception, config.get, 'foo' )
        config.set(['foo'],'bar')
        assert(config.get('foo') == 'bar')

    def test_nested_set(self):
        self.assertRaises( Exception, config.get, 'not', 'a', 'key' )
        config.set(['not','a','key'], 'bar' )
        assert(config.get('not','a','key') == 'bar')

if __name__ == '__main__':
    unittest.main()
