import yaml

from event_calendar.config import Singleton

codes = yaml.load( open('config/language_codes.yaml','r'), Loader=yaml.FullLoader )
languages = codes['LanguageCode']['enum'];

class LanguageException(Exception):

    def __init__(self,lang):
        self.message = 'Unrecognized language(s) {}'.format(lang)

class SiteSettings(metaclass=Singleton):

    def __init__(self):

        self._settings = {}

        try:
            with open("data/site.yaml",'r') as settings_file:
                self._settings = yaml.load(settings_file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            with open("data/site.default.yaml",'r') as settings_file:
                self._settings = yaml.load(settings_file, Loader=yaml.FullLoader)
                self.save()

    def save(self):
        with open("data/site.yaml",'w') as settings_file:
            yaml.dump(self._settings, settings_file)

    @property
    def default_language(self):
        return self._settings['default_language']

    @default_language.setter
    def default_language(self,lang):
        if lang in languages:
            self._settings['default_language'] = lang
        else:
            raise LanguageException( lang )

    @property
    def languages(self):
        return self._settings['languages']

    @languages.setter
    def languages(self,langs):
        bad_langs = [ lang for lang in langs if lang not in languages ]
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
    def info(self,lang):
        if lang:
            if lang in languages:
                return self._settings['info'][lang] or {}
            else:
                raise LanguageException(lang)
        else:
            return self._settings['info'] or {}

    @info.setter
    def info(self,info,lang):
        if lang:
            if lang in languages:
                self._validate_info(dict(zip((lang),(info))))
                self._settings['info'][lang] = info
            else:
                raise LanguageException(lang)
        else:
            self._validate_info(info)
            self._settings['info'] = info

    def _validate_info(self,info):
        for lang,data in info.items():
            if lang not in languages:
                raise LanguageException(lang)
            if not isinstance(x,dict):
                raise Exception('Site info must be a dict')

site_settings = SiteSettings()