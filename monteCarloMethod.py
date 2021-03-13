import numpy as np
from scipy import stats


def monte_carlo_generate(data, m, alpha, random_seed):
    mu = np.mean(data)
    sigma = np.std(data)

    # 一般情况下不会出现验证不通过， 循环一定会被跳出
    loop_num = 100
    while loop_num > 0:
        loop_num -= 1
        if random_seed:
            np.random.seed(loop_num)
        new_data = np.random.normal(mu, sigma, m)

        # 对新生成的数据的均值
        new_mu = np.mean(new_data)
        # 求置信区间
        conf_interval = stats.norm.interval(alpha, mu, sigma)
        if conf_interval[0] < new_mu < conf_interval[1]:
            return new_data
    return []
