import numpy as np
import math


def check_by_std(data, num_of_data):

    data = data - np.mean(data)
    theta_1 = math.sqrt(np.sum(np.power(data, 2))/(num_of_data - 1))
    theta_2 = 1.253 * np.sum(np.abs(data)) / math.sqrt(num_of_data * (num_of_data - 1))

    u = math.fabs(theta_1 / theta_2 - 1)
    std_u = 2 / math.sqrt(num_of_data - 1)

    if u >= std_u:
        return False
    else:
        return True


