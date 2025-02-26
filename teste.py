import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# plt.figure()

df = pd.read_csv("data\\LUT_batt.csv", sep = ";")
# plt.plot(df["SoC"], df["Tensao"])
# plt.show()





print(f"df['SoC'] = {df['SoC']}")
print(np.cumsum(df['SoC']))