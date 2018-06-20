from urllib.parse import urlencode
from .json_request import json_request
from datetime import datetime
import math

END_POINT = 'http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList'
# SERVICE_KEY = '10wfesCEKZKTWb9IhpFWutS0D6Z6p2M1j9BlDf0VCuhfzvsI74IuQND3AgnhxdIpSyI9lER%2FH55iva04jaZEtA%3D%3D'

def pd_gen_url(
        endpoint = END_POINT,
        serviceKey = '',
        **params):
    url = '%s?serviceKey=%s&%s' % (endpoint, serviceKey, urlencode(params))  # urlencode하면 다 escape를 하므로 서비스 키 내용이 달라짐
    return url

# def pd_fetch_tourspot_visitor(district1='', district2='', tourspot='', year=0, month=0):
#     url = pd_gen_url(endpoint = END_POINT,
#                      serviceKey=SERVICE_KEY,
#                      SIDO=district1,
#                      GUNGU=district2,
#                      RES_NM=tourspot,
#                      YM='{0:04d}{1:02d}'.format(year, month),
#                      _type = 'json',
#                      numOfRows=20
#                      )
#     json_result = json_request(url=url)
#
#     json_response = json_result.get('response')
#     json_header = json_response.get('header')
#     result_message = json_header.get('resultMsg') # 헤더를 제대로 불러오는지 판단하기 위한 파라미터
#
#     if 'OK' != result_message:
#         print('%s Error[%s] for request %s' % (datetime.now(), result_message, url)) # 에러나면 에러메세지 출력
#         return None
#     #여기까지 왔다는건 헤더를 불러오는데 성공했다는 것
#     json_body =  json_response.get('body')
#     json_items = json_body.get('items')
#
#     yield json_items.get('item')

 # 페이징 의사코드

def pd_fetch_tourspot_visitor(district1='', district2='', tourspot='', year=0, month=0, service_key=''):
    pageno=1
    hasnext=True
    while hasnext:
        url = pd_gen_url(endpoint = END_POINT,
                         serviceKey=service_key,
                         SIDO=district1,
                         GUNGU=district2,
                         RES_NM=tourspot,
                         YM='{0:04d}{1:02d}'.format(year, month),
                         _type = 'json',
                         numOfRows=10,
                         pageNo=pageno)
        json_result = json_request(url=url)

        json_response = json_result.get('response')
        json_body = json_response.get('body')
        numofrows = json_body.get('numOfRows')
        totalcount = json_body.get('totalCount')
        json_items = json_body.get('items')

        if totalcount == 0 :
            break
        last_page = math.ceil(totalcount/numofrows)
        if pageno == last_page:
            hasnext = False
        else:
            pageno += 1
        yield json_items.get('item')

def pd_fetch_foreign_visitor(country_code, year, month, service_key=''):
    endpoint = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    url = pd_gen_url(
        endpoint,
        service_key,
        YM='{0:04d}{1:02d}'.format(year, month),
        NAT_CD=country_code,
        ED_CD='E',
        _type='json')
    json_result = json_request(url=url)

    json_response = json_result.get('response')
    json_header = json_response.get('header')
    result_message = json_header.get('resultMsg')
    if 'OK' != result_message:
        print('%s Error[%s] for request %s' % (datetime.now(), result_message, url))
        return None

    json_body = json_response.get('body')
    json_items = json_body.get('items')

    return json_items.get('item') if isinstance(json_items, dict) else None
