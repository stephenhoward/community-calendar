import unittest
import event_calendar.query_builder
from event_calendar.model.event import Event

valid_variations = [
    ( 'bar',          [None, 'bar','eq'] ),
    ( 'baz[gt]',      [None, 'baz','gt'] ),
    ( 'bar.baz',      ['bar','baz','eq'] ),
    ( 'bar.baz[lte]', ['bar','baz','lte'] )
]

class TestQueryBuilder(unittest.TestCase):

    def test_parse_valid_param(self):

        for variation in valid_variations:

            with self.subTest( variation[0][1] ):
                rel_name, rel_attr, operator = event_calendar.query_builder._parse_parameter( variation[0] )
                self.assertEqual( rel_name, variation[1][0] )
                self.assertEqual( rel_attr, variation[1][1] )
                self.assertEqual( operator,   variation[1][2] )

    def test_parse_invalid_param(self):

        self.assertRaises( event_calendar.query_builder.QueryFormatException, event_calendar.query_builder._parse_parameter, 'bar.baz.qux' )
        self.assertRaises( event_calendar.query_builder.QueryFormatException, event_calendar.query_builder._parse_parameter, 'bar(gt)' )
        self.assertRaises( event_calendar.query_builder.QueryFormatException, event_calendar.query_builder._parse_parameter, 'bar.baz.qux[gt]' )

    def test_parse_parameters(self):
        q = event_calendar.query_builder.query_from_query_string( Event, **{ 'status': 'Active' } )
        self.assertNotEqual(q,None)
        q = event_calendar.query_builder.query_from_query_string( Event, **{ 'dates.start_time[gt]': '2020-09-04' } )
        self.assertNotEqual(q,None)

    def test_parse_bad_parameters(self):
        self.assertRaises( Exception, event_calendar.query_builder.query_from_query_string, Event, **{ 'noattr': 'foo' } )
        self.assertRaises( Exception, event_calendar.query_builder.query_from_query_string, Event, **{ 'norel.start_time[gt]': '2020-09-04' } )
