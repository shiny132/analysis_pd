import collection
from matplotlib import font_manager, rc
import analyze
# if __name__ == '__main__':
#     collection.crawlling_tourspot_visitor(district='서울특별시', start_year=2017, end_year=2017)
import collection
from config import CONFIG
import visualize
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    resultfiles = dict()

    #collect
    resultfiles['tourspot_visitor'] = collection.crawling_tourspot_visitor(
        district=CONFIG['district'],
        **CONFIG['common'])

    resultfiles['foreign_visitor'] = []
    for country in CONFIG['countries']:
        rf = collection.crawling_foreign_visitor(country, **CONFIG['common'])
        resultfiles['foreign_visitor'].append(rf)

    # 1. analysis and visualize
    # result_analysis = analyze.analysis_correlation(resultfiles)
    # visualize.graph_scatter(result_analysis)

    # 2. analysis and visualize
    font_filename = 'c:/Windows/fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=font_filename).get_name()
    font_options = {'family': 'Malgun Gothic'}
    plt.rc('font', **font_options)
    plt.rc('axes', unicode_minus=False)

    result_analysis = analyze.analysis_correlation_by_tourspot(resultfiles) # 각 관광명소와 각 나라 관광객들의 상관계수 ex)창덕궁 방문자 수와 일본 관광객의 상관계수
    print(result_analysis)
    graph_table = pd.DataFrame(result_analysis, columns=['tourspot', 'r_중국', 'r_일본', 'r_미국'])
    graph_table = graph_table.set_index('tourspot')

    graph_table.plot(kind='bar')
    plt.show()