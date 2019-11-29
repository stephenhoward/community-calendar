import yaml

from event_calendar.config import Singleton
from event_calendar.model.user import User

languages = yaml.load( open('config/languages.yaml','r'), Loader=yaml.FullLoader )
codes = list(languages.keys())

class LanguageException(Exception):

    def __init__(self,lang):
        self.message = 'Unrecognized language(s) {}'.format(lang)

class SiteSettings(metaclass=Singleton):

    def __init__(self):

        self._settings = {}

        try:
            with open("/var/calendar/data/site.yaml",'r') as settings_file:
                self._settings = yaml.load(settings_file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            with open("config/site.default.yaml",'r') as settings_file:
                self._settings = yaml.load(settings_file, Loader=yaml.FullLoader)
                self.save()

    def dump(self):
        s     = self._settings
        setup = self.needs_setup

        if setup:
            s['needs_setup'] = 1
        else:
            s.pop('needs_setup',None)

        return s

    def update_values(self,**kwargs):

        for setting in kwargs:

            if setting == 'info':
                for lang in kwargs['info']:
                    self.set_info( lang['language'], lang )
            else:
                setattr(self, setting, kwargs[setting])

    def save(self):
        with open("/var/calendar/data/site.yaml",'w') as settings_file:
            yaml.dump(self._settings, settings_file)

    @property
    def default_language(self):
        return self._settings['default_language']

    @default_language.setter
    def default_language(self,lang):
        if lang in codes:
            self._settings['default_language'] = lang
        else:
            raise LanguageException( lang )

    @property
    def languages(self):
        return self._settings['languages']

    @languages.setter
    def languages(self,langs):
        bad_langs = [ lang for lang in langs if lang not in codes ]
        if len(bad_langs):
            raise LanguageException( ', '.join(bad_langs) )
        else:
            self._settings['languages'] = langs

    @property
    def splash_image(self):
        filename = self._settings['splash_image']
        if ( filename ):
            return SiteImage(filename = filename)
        else:
            return None

    @splash_image.setter
    def splash_image(self,Image):
        if Image == None:
            self._settings['splash_image'] = None
        else:
            self._settings['splash_image'] = SiteImage.filename

    @property
    def from_email(self):
        if 'from_email' in self._settings:
            return self._settings['from_email']
        else:
            return 'sender@example.com'

    @from_email.setter
    def from_email(self,email_address):
        self._settings['from_email'] = email_address

    @property
    def needs_setup(self):
        user_count = User.search().count()
        if user_count > 0:
            return None

        return 1

    @needs_setup.setter
    def needs_setup(self,value):
        # no-op
        return None

    def info(self,lang):
        if lang:
            if lang in codes:
                return self._settings['info'][lang] or {}
            else:
                raise LanguageException(lang)
        else:
            return self._settings['info'] or {}

    def set_info(self,lang,info):
        if lang:
            if lang in codes:
                self._validate_info(dict(zip([lang],[info])))
                self._settings['info'][lang] = info
            else:
                raise LanguageException(lang)
        else:
            self._validate_info(info)
            self._settings['info'] = info

    def _validate_info(self,info):
        for lang,data in info.items():
            if lang not in codes:
                raise LanguageException(lang)
            if not isinstance(data,dict):
                raise Exception('Site info must be a dict')
            for key,value in data.items():
                if not isinstance( value, str ):
                    raise Exception( '"' + key + '" ('+ lang +'): translatable values must be strings')
                if key not in ['language','site_title']:
                    raise Exception( '"' + key + '" is not a permitted translatable site setting')

site_settings = SiteSettings()