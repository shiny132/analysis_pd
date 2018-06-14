# http test
from urllib.request import Request, urlopen
from datetime import *
import sys
import json

try:
    url = 'http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList'
    request = Request(url)
    resp = urlopen(request)
    resp_body = resp.read().decode("utf-8")
    print(type(resp_body), ":", resp_body)

    json_result = json.loads(resp_body) # json 형식으로 body 읽어들임
    print(type(json_result), ":", json_result) # 타입은 dictionary로 들어옴

    data = json_result['data'] # json load 한 data만 따로 data에 저장
    print(type(data), ":", data) # data만 따로 딴 것은 list로 저장됨

except Exception as e:
    print('%s %s' % (e, datetime.now()), file=sys.stderr)