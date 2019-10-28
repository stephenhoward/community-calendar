from jinja2 import Environment, FileSystemLoader
import os

class Templates (Environment):

    def get_template(self,name,**kwargs):

        lang = kwargs.pop('lang','en')
        name = os.path.join(lang,name)

        return super().get_template(name,**kwargs)

templates = Templates(
    loader = FileSystemLoader('/opt/calendar/templates')
)
