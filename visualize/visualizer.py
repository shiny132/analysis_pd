import matplotlib.pyplot as plt
import analyze
def graph_scatter(result_analysis):
    fig, subplots = plt.subplots(1, len(result_analysis), sharey=True)

    for index, result in enumerate(result_analysis):
        # subplots[index].scatter(result['x'], result['y'])
        subplots[index].set_xlabel('{0}인 입국자수'.format(result['country_name']))
        index == 0 and subplots[index].set_ylabel('관광지 입장객 수')
        subplots[index].set_title('r={:.5f}'.format(result['r']))
        subplots[index].scatter(result['x'], result['y'], c='black', s=6) # s = 사이즈 / c = 컬러
        plt.subplots_adjust(wspace=0) # 그래프들간의 간격 없애기
    plt.show()

def graph_scatter2(result_analysis):
    fig, subplots = plt.subplots(1, len(result_analysis), sharey=True)

    for index, result in enumerate(result_analysis):
        # subplots[index].scatter(result['x'], result['y'])
        subplots[index].set_xlabel('{0}인 입국자수'.format(result['country_name']))
        index == 0 and subplots[index].set_ylabel('관광지 입장객 수')
        subplots[index].set_title('r={:.5f}'.format(result['r']))
        subplots[index].scatter(result['x'], result['y'], c='black', s=6)  # s = 사이즈 / c = 컬러
        plt.subplots_adjust(wspace=0)  # 그래프들간의 간격 없애기
    plt.show()