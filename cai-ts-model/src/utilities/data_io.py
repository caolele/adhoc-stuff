import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# def get_train_data_by_date(data: pd.DataFrame, date: str):
#     return data[date, :]


def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y%m%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYYMMDD")


def get_prev_n_dates(target_date: datetime, n_day: int):
    day_list = []
    for i in range(n_day):
        day_i = target_date - timedelta(days=i + 1)
        day_list.append(day_i.strftime("%Y%m%d"))
    return day_list


def add_noise(data: np.ndarray):
    noise = np.random.normal(-1, 1, data.shape) * 1e-8
    return data + noise


def get_one_ts_sample(data: pd.DataFrame, label_date: str, n_day: int):

    num_features = data.shape[-1]

    valid_dates = data.index.get_level_values("date")
    prev_n_days = get_prev_n_dates(validate_date(label_date), n_day)
    ts_sample = np.array([])
    last_date_samples = None
    # print(label_date, prev_n_days)
    for dt in prev_n_days:
        if dt in valid_dates:
            last_date_samples = data.loc[dt, :]
        elif last_date_samples is None:
            raise KeyError("Error! Missing date from dataset: " + dt)

        # add month and day as one of the features
        _sampled_month_norm = float(dt[4:6]) / 12.0
        _sampled_day_norm = float(dt[6:]) / 31.0
        # _sampled = last_date_samples.sample().as_matrix()[0]
        _sampled = np.diag(last_date_samples.sample(num_features).as_matrix())
        # print(_sampled)
        _sampled = np.concatenate((_sampled, np.array([_sampled_month_norm, _sampled_day_norm])))

        # add current sample to time-series
        if ts_sample.shape[0] == 0:
            ts_sample = np.array([add_noise(_sampled)])
        else:
            ts_sample = np.append(ts_sample, [add_noise(_sampled)], axis=0)

    # print(ts_sample.shape)
    return ts_sample


def get_one_batch(data: pd.DataFrame, label: pd.DataFrame, bs: int, n_day: int):

    cur_batch_data = np.array([])
    cur_batch_label = np.array([])
    cur_batch_case = np.array([])

    for spl in range(bs):
        # obtain labels info
        cur_label = label.sample()
        cur_case = cur_label.index.get_level_values("case").tolist()[0]
        cur_label_date = cur_label.index.get_level_values("date").tolist()[0]

        # obtain features
        cur_ts_data = get_one_ts_sample(data, cur_label_date, n_day)

        # insert into batch
        if cur_batch_data.shape[0] == 0:
            cur_batch_data = np.array([cur_ts_data])
            cur_batch_label = np.array([cur_label.as_matrix()[0]])
            cur_batch_case = np.array([[cur_case]])
        else:
            cur_batch_data = np.concatenate((cur_batch_data, [cur_ts_data]))
            cur_batch_label = np.concatenate((cur_batch_label, [cur_label.as_matrix()[0]]))
            cur_batch_case = np.concatenate((cur_batch_case, [[cur_case]]))

    return cur_batch_data, cur_batch_case, cur_batch_label