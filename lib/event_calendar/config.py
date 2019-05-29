import yaml

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs ):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,**kwargs)

        return cls._instances[cls]

class Config(metaclass=Singleton):
    _config = {}

    def __init__(self):

        with open("config/app.yaml",'r') as config_file:
            self._config = yaml.load(config_file)

    def get(self,*path):
        value = self._config
        for key in path:
            if key in value:
                loc = value[key]
            else:
                raise Exception('invalid config path: ' + path )

        return loc

    def set(self,path, value):
        path_range = range(len(path))
        dict       = self._config

        for i in path_range:
            key = path[i]

            if ( i == path_range ):
                dict[key] = value
            else:
                if key not in dict:
                    dict[key] = {}
                dict = dict[key]


config = Config()