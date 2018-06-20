import os
from collection.api.api import *
import json

# RESULT_DIRECTORY = '__result__/crawling/'

def preprocess_tourspot_visitor(post):
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

def preprocess_foreign_visitor(data):
    # ed
    del data['ed']

    # edCd
    del data['edCd']

    # rnum
    del data['rnum']

    #나라 코드
    data['country_code'] = data['natCd']
    del data['natCd']

    #나라 이름
    data['country_name'] = data['natKorNm'].replace(' ', '')
    del data['natKorNm']

    #방문자 수
    data['visit_count'] = data['num']
    del data['num']

    # 년월
    if 'ym' not in data:
        data['date'] = ''
    else:
        data['date'] = data['ym']
        del data['ym']


def crawling_tourspot_visitor(
        district,
        start_year,
        end_year,
        fetch=True,
        result_directory='',
        service_key=''):
    results = []
    filename = '%s/%s_tourspot_%s_%s.json' % (result_directory, district, start_year, end_year)

    if fetch:
        for year in range(start_year, end_year+1):
            for month in range(1, 13):
                for items in pd_fetch_tourspot_visitor(
                        district1=district,
                        year=year,
                        month=month,
                        service_key=service_key):
                    for item in items:
                        preprocess_tourspot_visitor(item)

                    results += items

        # save data to file
        with open(filename, 'w', encoding='utf-8') as outfile:
            json_string = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(json_string)

    return filename

def crawling_foreign_visitor(
        country,
        start_year,
        end_year,
        fetch=True,
        result_directory='',
        service_key=''):

    results = []
    filename = '%s/%s(%s)_foreignvisitor_%s_%s.json' % (result_directory, country[0], country[1], start_year, end_year)

    if fetch:
        for year in range(start_year, end_year+1):
            for month in range(1, 13):
                data = pd_fetch_foreign_visitor(
                    country[1],
                    year,
                    month,
                    service_key)
                if data is None:
                    continue

                preprocess_foreign_visitor(data)
                results.append(data)

        # save data to file
        with open(filename, 'w', encoding='utf-8') as outfile:
            json_string = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(json_string)
    return filename
# if os.path.exists(result_directory) is False:
#     os.makedirs(result_directory)


# def crawling_tourspot_visitor(district="서울특별시", start_year=0, end_year=0):
#     results = []
#     filename = '%s%s_touristspot_%s_%s.json' % (RESULT_DIRECTORY,
#         district,
#         start_year,
#         end_year)
#
#     for ye in range(start_year, end_year+1):
#         for mon in range(1, 13):
#             for posts in pd_fetch_tourspot_visitor(district, year = ye, month = mon):
#                 for post in posts:
#                     preprocess_post(post)
#                 results += posts
#
#     with open(filename, 'w', encoding='utf-8') as outfile:
#         json_string = json.dumps(
#             results,
#             indent=4,
#             sort_keys=True,
#             ensure_ascii=False)
#         outfile.write(json_string)
#
# if os.path.exists(RESULT_DIRECTORY) is False:
#     os.makedirs(RESULT_DIRECTORY)