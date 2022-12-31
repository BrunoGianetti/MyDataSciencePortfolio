import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("AlturaPresidente.csv")
print(data.head())

print(" " * 80)
print("X" * 80)
print(" " * 80)

height = np.array(data["height(cm)"])
print(height)

print(" " * 80)
print("X" * 80)
print(" " * 80)

print("Mean of heights =", height.mean())
print("Standard Deviation of height =", height.std())
print("Minimum height =", height.min())
print("Maximum height =", height.max())

print(" " * 80)
print("X" * 80)
print(" " * 80)

print("25th percentile =", np.percentile(height, 25))
print("Median =", np.median(height))
print("75th percentile =", np.percentile(height, 75))

print(" " * 80)
print("X" * 80)
print(" " * 80)

sns.set()
plt.hist(height)
plt.title("Height Distribution of Presidents of USA")
plt.xlabel("height(cm)")
plt.ylabel("Number")
plt.show()