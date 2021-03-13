import dataRead
import sysErrorCheck
import normalityTest
import grubbsAbnormalDetection
import monteCarloMethod
import gm11

import numpy as np
import os

# # 数据表格所在路径
# path = 'data.xlsx'
#
# # 读取数据列数
# index_of_data = 1
#
# # 显著性水平
# alpha = 0.01
# # alpha = 0.05
#
# # 模拟m个数据
# m = 100
# # 设为True则使得随机生成的数据可以复现
# random_seed = True


class Result:
    def __init__(self, success=False, string=None, abnormal_list=None,
                 generated_data=None, mean=None, std=None, mean_type=None):
        self.success = success
        self.string = string
        self.abnormal_list = abnormal_list
        self.generated_data = generated_data
        self.mean = mean
        self.std = std
        self.mean_type = mean_type


def calculate(path, index_of_sheet, index_of_row, alpha, m, output, random_seed=True):
    result = Result()
    # 读取数据
    data = dataRead.read_by_excel(path, index_of_sheet, index_of_row)
    data = np.array(data)
    num_of_data = data.size

    # 检测是否存在系统误差
    whether_qualified = sysErrorCheck.check_by_std(data, num_of_data)
    # 存在系统误差则输出重新测量提示并异常退出
    if not whether_qualified:
        result.string = "存在系统误差"
        return result

    # 根据数据量大小做正态性检验
    check_return = normalityTest.normality_test(data, num_of_data, alpha)
    if check_return != 4:
        if check_return == 1:
            result.string = "过多数据"

        elif check_return == 2:
            result.string = "过少数据"

        elif check_return == 3:
            result.string = "不符合正态分布"
        return result

    # 插入异常数据作为测试
    # data = np.append(data, [200, 199, 1], axis=0)

    # Grubbs 检验粗大误差
    data, abnormal_list = grubbsAbnormalDetection.abnormal_detection(data)
    result.abnormal_list = abnormal_list
    if len(abnormal_list) > 0:
        # 再进行一次系统误差和正态性检验
        # 检测是否存在系统误差
        whether_qualified = sysErrorCheck.check_by_std(data, num_of_data)
        # 存在系统误差则输出重新测量提示并异常退出
        if not whether_qualified:
            result.string = "存在系统误差"
            return result

        # 根据数据量大小做正态性检验
        check_return = normalityTest.normality_test(data, num_of_data, alpha)
        if check_return != 4:
            if check_return == 1:
                result.string = "过多数据"
            elif check_return == 2:
                result.string = "过少数据"
            elif check_return == 3:
                result.string = "不符合正态分布"
            return result

    # gm_11模型生成数据的附加
    if num_of_data < 500:
        data = np.append(data, gm11.gm11(data), axis=0)

    # 蒙特卡洛模拟及检验
    new_data = monteCarloMethod.monte_carlo_generate(data, m, alpha, random_seed)
    if len(new_data) > 0:
        result.success = True
        result.generated_data = new_data
        mean = np.mean(new_data)
        mean_data = new_data[new_data < mean]
        if output == 1:
            result.mean = str(np.mean(mean_data))
            result.mean_type = "先进水平"
        elif output == 2:
            result.mean = str(np.mean([mean, np.mean(mean_data)]))
            result.mean_type = "平均先进水平"
        elif output == 3:
            result.mean = str(mean)
            result.mean_type = "平均水平"

        result.std = str(np.std(new_data))
        result.string = "计算成功， 计算结果均值为"+result.mean
    else:
        result.string = "不能生成合适的数据"

    return result


if __name__ == '__main__':
    result = calculate("D:/codes/python/QTwork/data.xlsx",  0, 1, 0.05, 100, 3)
    print(result.string)
