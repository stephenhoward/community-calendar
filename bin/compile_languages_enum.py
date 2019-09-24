import yaml

enum_codes = {
    'LanguageCode': {
        'type': 'string',
        'enum': []
    }
}

codes = yaml.load( open('config/languages.yaml','r'), Loader=yaml.FullLoader )

for code in codes:
    enum_codes['LanguageCode']['enum'].append(code)

with open('config/language_codes.yaml', 'w') as f:
    yaml.dump(enum_codes, f)