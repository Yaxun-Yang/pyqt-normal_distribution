import numpy as np
from pandas import Series
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt


def gm11(data):
    data = np.sort(data)
    a = identification_algorithm(data)
    xk = gm_model(data, a)
    xk = my_return(xk)
    return xk


def identification_algorithm(x):    # 辨识算法
    b = np.array([[1]*2]*(len(x) - 1))
    tmp = np.cumsum(x)
    for i in range(len(x)-1):
        b[i][0] = (tmp[i] + tmp[i+1]) * (-1.0) / 2
    y = np.transpose(x[1:])
    bt = np.transpose(b)
    a = np.linalg.inv(np.dot(bt, b))
    a = np.dot(a, bt)
    a = np.dot(a, y)
    a = np.transpose(a)
    return a


def gm_model(x0, a):          # GM(1,1)模型
    a_big = np.ones(len(x0))
    for i in range(len(a_big)):
        a_big[i] = a[1]/a[0] + (x0[0]-a[1]/a[0])*np.exp(a[0]*(i+1)*(-1))  # i+1 or i

    return a_big


def my_return(xk):  # 预测值还原
    tmp = np.ones(len(xk))
    for i in range(len(xk)):
        if i == 0:
            tmp[i] = xk[i]
        else:
            tmp[i] = xk[i] - xk[i-1]
    return tmp
