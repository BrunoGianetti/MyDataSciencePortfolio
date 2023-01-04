import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

births = pd.read_csv("births.csv")
print(births.head())
births['day'].fillna(0, inplace= True)
births['day'] = births['day'].astype(int)

print(' ' * 80)
print('X' * 80)
print(' ' * 80)

births['decade'] = 10 * (births['year'] // 10)
births.pivot_table('births', index = 'decade', columns='gender', aggfunc='sum')
print(births.head())

print(' ' * 80)
print('X' * 80)
print(' ' * 80)

sns.set()
birth_decade = births.pivot_table('births', index = 'decade', columns='gender', aggfunc='sum')
birth_decade.plot()
plt.ylabel("Total births per year")
#plt.show() I have only one plt.show() and must be in the finish of script

########################################################################################

quartiles = np.percentile(births['births'], [25, 50, 75])
mu = quartiles[1]
sig = 0.74 * (quartiles[2] - quartiles[0])

births = births.query('(births > @mu - 5 * @sig) & (births < @mu + 5 * @sig)')
births['day'] = births['day'].astype(int)
births.index = pd.to_datetime(
    10000 * births.year +
    100 * births.month +
    births.day, format = '%Y%m%d'
)
births['dayofweek'] = births.index.dayofweek

births.pivot_table('births',
                   index = 'dayofweek',
                   columns = 'decade',
                   aggfunc = 'mean'
                   ).plot()
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
plt.ylabel('mean births by day')
#plt.show() I have only one plt.show() and must be in the finish of script

# The graphs don't work simultaneously.

#######################################################################################

births_month = births.pivot_table('births', [births.index.month, births.index.day])
print(births_month.head())

births_month.index = [pd.datetime(2012, month, day) for (month, day) in births_month.index]
print(births_month.head())

print(' ' * 80)
print('X' * 80)
print(' ' * 80)

fig, ax = plt.subplots(figsize = (12,4))
births_month.plot(ax=ax)
plt.show()