import pandas as pd
import matplotlib.pyplot as plt

plt.figure()

df = pd.read_csv("data\\LUT_batt.csv", sep = ";")
plt.plot(df["SoC"], df["Tensao"])
plt.show()