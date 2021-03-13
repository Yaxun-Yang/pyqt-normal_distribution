import scipy.stats as stats


def normality_test(data, num_of_data, alpha):
    # 直接调库实现
    if num_of_data > 1000:
        return 1
    elif num_of_data > 50:
        p_value = stats.normaltest(data)[1]
    elif num_of_data >= 8:
        p_value = stats.shapiro(data)[1]
    else:
        return 2

    if p_value > alpha:
        return 4
    else:
        return 3
