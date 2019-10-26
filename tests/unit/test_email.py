import unittest
from unittest.mock import patch
from event_calendar.email import EmailSender
from email.message import EmailMessage
from event_calendar.templates import templates
from jinja2 import Template
import smtplib
import pprint

class TestEmail(unittest.TestCase):

    def test_sendEmail(self):

        kwargs = {
            'subject': "Subject Line",
            'message': "Message Body",
            'to':      "recipient@example.com",
            'from':    "sender@example.com"        
        }

        with patch("smtplib.SMTP") as mock_smtp:
            sender = EmailSender()

            sender.send_email( **kwargs )

            smtp    = mock_smtp.return_value
            message = smtp.send_message.call_args[0][0]

            smtp.send_message.assert_called_once()
            self.assertTrue( isinstance(message, EmailMessage) )
            self.assertEqual( message['To'],         kwargs['to'] )
            self.assertEqual( message['From'],       kwargs['from'] )
            self.assertEqual( message['Subject'],    kwargs['subject'] )
            self.assertEqual( message.get_content(), kwargs['message'] + "\n" )

    def test_sendTemplatedEmail(self):

        kwargs = {
            'template': "Subject Line\n----\nMessage Body",
            'to':       "recipient@example.com",
            'from':     "sender@example.com",
            'args':     {}       
        }

        with patch("smtplib.SMTP") as mock_smtp:
            with patch.object(templates,"get_template", return_value = Template(kwargs['template']) ):
                sender = EmailSender()

                sender.send_template( **kwargs )

                message = mock_smtp.return_value.send_message.call_args[0][0]

                self.assertEqual( message['To'],         kwargs['to'] )
                self.assertEqual( message['From'],       kwargs['from'] )
                self.assertEqual( message['Subject'],    'Subject Line' )
                self.assertEqual( message.get_content(), "Message Body\n" )

if __name__ == '__main__':
    unittest.main()