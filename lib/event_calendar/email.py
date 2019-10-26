from event_calendar.templates import templates
from event_calendar.config import config
from event_calendar.site_settings import site_settings
from email.message import EmailMessage
import smtplib
import ssl

default_context = ssl.create_default_context()


class EmailSender: 

    def __init__(self):
        with open('/var/calendar/secrets/email.txt', 'rb') as fh:
            (user,password) = fh.read().decode('utf-8').split(':')
            self._user      = user
            self._password  = password
            self._session   = smtplib.SMTP(config.get('email','server'))

    def _get_session(self):

        self._session.starttls( context = default_context )

        return self._session

    def send_email(self,**kwargs):
            msg = EmailMessage()
            msg['Subject'] = kwargs['subject']
            msg['From']    = kwargs['from'] or site_settings.from_email
            msg['To']      = kwargs['to']

            msg.set_content(kwargs['message'])

            s = self._get_session()
            s.send_message(msg)
            s.quit()

    def send_template(self,**kwargs):

            (subject,message) = templates \
                .get_template(kwargs['template']) \
                .render( **kwargs['args'] ) \
                .split("\n----\n")

            kwargs['subject'] = subject
            kwargs['message'] = message

            self.send_email(**kwargs)
