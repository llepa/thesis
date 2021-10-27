import pandas as pd
import numpy as np
import statsmodels.stats.weightstats as ws

def m1(T, n):
    sum = 0
    for t in T:
        sum += t**n
    sum /= len(T)
    return sum


def cm1(T, n):
    s = m1(T, 1)
    sum = 0
    for t in T:
        sum += (t - s)**n
    sum /= len(T)
    return sum


def iter(df, n):
    out = []
    for col in df.head():
        if (type(df[col].iloc[0]) == np.int64 or type(df[col].iloc[0]) == np.float64):
            out.append(m1(df[col].to_numpy(), n))
    return out


def citer(df, n):
    out = []
    for col in df.head():
        if (type(df[col].iloc[0]) == np.int64 or type(df[col].iloc[0]) == np.float64):
            out.append(cm1(df[col].to_numpy(), n))
    return out


def corr(df):
    cols = list()
    for col in df.columns:
        if (type(df[col].iloc[0]) == np.int64 or type(df[col].iloc[0]) == np.float64):
            cols.append(col)
    d1 = ws.DescrStatsW(df[list(cols)])
    # return np.ndarray object type
    return d1.corrcoef


# TEST
"""
c = pd.read_csv('smart_grid_stability_augmented.csv')
print(c)
print()
print("Mean:")
print(iter(c,1))
print()
print("Variance:")
print(citer(c,2))
print()
print("Correlation:")
print(corr(c)) """