import unittest
from unittest.mock import patch
from event_calendar.email import EmailSender
from email.message import EmailMessage
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

if __name__ == '__main__':
    unittest.main()