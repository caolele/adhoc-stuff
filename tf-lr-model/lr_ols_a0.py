import numpy as np
import os
import pandas as pd

# from sklearn.datasets import load_boston
# from sklearn.linear_model import LinearRegression


def load_csv_data(file):
    if file[-4:] != ".csv":
        file += ".csv"
    if os.path.isfile(file):
        raw_data = pd.read_csv(file)
        hc_spend = raw_data["c2"]
        hc_spend_x_case_num = raw_data["c12"]
        raw_data["c2"] = (hc_spend - hc_spend.mean()) / hc_spend.std()
        raw_data["c12"] = (hc_spend_x_case_num - hc_spend_x_case_num.mean()) / hc_spend_x_case_num.std()
        label_hc_spend = raw_data["l1"]
        raw_data["l1"] = (label_hc_spend - label_hc_spend.mean()) / label_hc_spend.std()
        raw_data['bias'] = pd.Series(np.ones(len(raw_data['c1'])), index=raw_data.index)
        return raw_data[["iid"]], \
               raw_data[["c1", "c2", "c12", "bias"]], \
               raw_data[["l1"]]
    else:
        print("Error: Data file " + file + "not found!")
        exit(1)


if __name__ == '__main__':

    ids, features, labels = load_csv_data("data_sample")
    X = features.values
    y = labels.values

    w = np.dot(np.linalg.pinv(X), y)
    print('custom')
    print(w)