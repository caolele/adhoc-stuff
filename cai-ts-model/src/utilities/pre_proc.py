# from numpy import genfromtxt
# tsd = genfromtxt('../data/sensors_data.csv', delimiter=',')
# print(tsd)

import pandas as pd
import numpy as np


## pre-process data
def pre_process_data():
    # df = pd.DataFrame(raw_data, columns = ['dt', 'temp1', 'temp2', 'water1', 'water2', 'moi1', 'moi2', 'lutemp', 'co2', 'lux'])

    df = pd.read_csv('../data/sensors_data.csv', index_col='dt', names=[
        'dt', 'temp1', 'temp2', 'water1', 'water2', 'moi1', 'moi2', 'lutemp', 'co2', 'lux'])
    print(df.head(), '\n')

    data_mean = df.mean()
    data_std = df.std()
    print("DATA MEAN:\n", data_mean, '\n')
    print("DATA STDEV:\n", data_std, '\n')
    df_norm = (df - data_mean) / data_std

    # data_min = df.min()
    # data_max = df.max()
    # print("DATA MIN:\n", data_min, '\n')
    # print("DATA MAX:\n", data_max, '\n')
    # df_norm = (df - data_min) / (data_max - data_min)

    df_norm = df_norm.reset_index()
    df_norm[['dt']] = df_norm[['dt']].astype(str)

    df_norm['date'] = df_norm['dt'].str.slice(0, 8)
    df_norm['time'] = df_norm['dt'].str[8:]
    del df_norm['dt']
    df_norm = df_norm.set_index(['date', 'time'])

    print(df_norm, '\n')
    print(df_norm.dtypes, '\n')

    # dfq = df_norm.query("date=='20180117'")
    # print(dfq)

    # return df_norm, data_min, data_max
    return df_norm, data_mean, data_std


## pre-process label
def pre_process_label():
    ldf = pd.read_csv('../data/label.csv', index_col=['dt', 'case'], names=[
        'dt', 'case', 'dia', 'lev1', 'lev2', 'lev3', 'rph'])
    print(ldf.head(), '\n')

    label_mean = ldf.mean()
    label_std = ldf.std()
    print("LABEL MEAN:\n", label_mean, '\n')
    print("LABEL STDEV:\n", label_std, '\n')
    ldf_norm = (ldf - label_mean) / label_std

    # label_min = ldf.min()
    # label_max = ldf.max()
    # print("LABEL MIN:\n", label_min, '\n')
    # print("LABEL MAX:\n", label_max, '\n')
    # ldf_norm = (ldf - label_min) / (label_max - label_min)

    ldf_norm = ldf_norm.reset_index()
    ldf_norm[['dt']] = ldf_norm[['dt']].astype(str)

    ldf_norm['date'] = ldf_norm['dt'].str.slice(0, 8)
    del ldf_norm['dt']
    ldf_norm = ldf_norm.set_index(['case', 'date'])

    print(ldf_norm, '\n')
    print(ldf_norm.dtypes, '\n')

    # return ldf_norm, label_min, label_max
    return ldf_norm, label_mean, label_std
