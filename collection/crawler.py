import os
from collection.api.api import *
import json

RESULT_DIRECTORY = '__result__/crawling/'

def preprocess_post(post):
    # count_locals
    rm = ['gungu', 'sido', 'addrCd', 'ym', 'rnum', 'resNm', 'csForCnt', 'csNatCnt']

    if 'csNatCnt' not in post:
        post['count_locals'] = 0
    else:
        post['count_locals'] = post['csNatCnt']

    # count_forigner
    if 'csForCnt' not in post:
        post['count_forigner'] = 0
    else:
        post['count_forigner'] = post['csForCnt']

    # tourist_spot
    if 'resNm' not in post:
        post['tourist_spot'] = 0
    else:
        post['tourist_spot'] = post['resNm']

    # date
    if 'ym' not in post:
        post['date'] = 0
    else:
        post['date'] = post['ym']

    # 시도
    if 'sido' not in post:
        post['restrict1'] = 0
    else:
        post['restrict1'] = post['sido']

    # 군구
    if 'gungu' not in post:
        post['restrict2'] = 0
    else:
        post['restrict2'] = post['gungu']
    for delete in rm:
        if delete in post:
            del post[delete]


def crawlling_tourspot_visitor(district="서울특별시", start_year=0, end_year=0):
    results = []
    filename = '%s%s_touristspot_%s_%s.json' % (RESULT_DIRECTORY,
        district,
        start_year,
        end_year)

    for ye in range(start_year, end_year+1):
        for mon in range(1, 13):
            print(pd_fetch_tourspot_visitor(district, year=ye, month=mon))
            for posts in pd_fetch_tourspot_visitor(district, year = ye, month = mon):
                for post in posts:
                    preprocess_post(post)
                results += posts

    with open(filename, 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(
            results,
            indent=4,
            sort_keys=True,
            ensure_ascii=False)
        outfile.write(json_string)

if os.path.exists(RESULT_DIRECTORY) is False:
    os.makedirs(RESULT_DIRECTORY)
