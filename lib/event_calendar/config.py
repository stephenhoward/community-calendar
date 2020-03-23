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
            self._config = yaml.load(config_file, Loader=yaml.FullLoader)

    def get(self,*path):
        value = self._config
        for key in path:
            if key in value:
                value = value[key]
            else:
                raise Exception('invalid config path: ' + '/'.join(path) )

        return value

    def set(self,path, value):
        path_range = range(len(path))
        path_max   = path_range[-1]
        dict       = self._config

        for i in path_range:
            key = path[i]

            if ( i == path_max ):
                dict[key] = value
            else:
                if key not in dict:
                    dict[key] = {}
                dict = dict[key]


config = Config()
