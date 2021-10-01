import pandas as pd
import numpy as np
import statsmodels.stats.weightstats as ws
import statsmodels.stats.descriptivestats as ds

np.set_printoptions(suppress=True)

df = pd.read_csv("./smart_grid_stability_augmented.csv")
print(df)
print()

d1 = ws.DescrStatsW(df[list(df.columns)[:13]])

print('Mean:')
print(d1.mean)
print()

print('Variance:')
print(d1.var)
print()

print('Correlation:')
print(d1.corrcoef)
print()

df = ds.describe(df[list(df.columns)[:13]], stats=['skew','kurtosis'])

print('Skewness:')
skew = df.loc[['skew']].values
print(skew)
print()

print('Kurtosis:')
kurt = df.loc[['kurtosis']].values
print(kurt)
print()


