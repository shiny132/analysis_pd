import os

# configuration
CONFIG = {
    'district': '서울특별시',
    'countries': [('중국', 112), ('일본', 130), ('미국', 275)],
    'common': {
        'start_year': 2017,
        'end_year': 2017,
        'fetch': False,
        'result_directory': '__results__/crawling',
        'service_key': '10wfesCEKZKTWb9IhpFWutS0D6Z6p2M1j9BlDf0VCuhfzvsI74IuQND3AgnhxdIpSyI9lER%2FH55iva04jaZEtA%3D%3D'
    }
}

if not os.path.exists(CONFIG['common']['result_directory']):
    os.makedirs(CONFIG['common']['result_directory'])