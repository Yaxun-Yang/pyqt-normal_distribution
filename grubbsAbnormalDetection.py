import smirnov_grubbs
import numpy as np


def abnormal_detection(data):
    abnormal_list = np.array([])
    while True:
        index = smirnov_grubbs.two_sided_test_indices(data)
        abnormal_list = np.append(abnormal_list, data[index])
        data = np.delete(data, index)

        if len(index) == 0:
            return data, abnormal_list
