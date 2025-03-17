import matplotlib.pyplot as plt
import pandas as pd
import os

fig_width_cm = 8/1.4
fig_height_cm = 3.54/1.4
params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern',
          'axes.labelweight' : 'bold'
          }
plt.rcParams.update(params)
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']


path = "resultados"
files = sorted(os.listdir(path), key=lambda x: int(x.split('_')[1].replace('kW.pkl', '')))
print(files)

fig, axs = plt.subplots(figsize=(fig_width_cm, fig_height_cm * 2), nrows=3, ncols=1, sharex=True)
i = 0
for file in files:
    df = pd.read_pickle(path + "\\" + file)
    # print(df)
    limiar = file.split("_")[1]
    axs[0].plot(df["Tempo"], df['SoC_bat'], linewidth = 2, color = colors[i], label = limiar.split(".")[0])
    axs[1].plot(df["Tempo"], df['v_banco_bat'], linewidth = 2, color = colors[i], label = limiar.split(".")[0])
    axs[2].plot(df["Tempo"], df['i_bat'], linewidth = 2, color = colors[i], label = limiar.split(".")[0])
    i += 1

axs[0].grid()
axs[0].set_ylabel(r"SoC [\%]", fontweight = 'bold')
axs[0].legend(loc='upper right')

axs[1].grid()
axs[1].set_ylabel("Tensão [V]", fontweight = 'bold')
axs[1].legend(loc='upper right')

axs[2].grid()
axs[2].set_ylabel("Corrente [A]", fontweight = 'bold')
axs[2].set_xlabel("Tempo [s]", fontweight = 'bold')
axs[2].set_xlim(df["Tempo"][0], df["Tempo"][len(df["Tempo"])-1])
axs[2].legend(loc='upper right')
plt.tight_layout()
plt.savefig("figuras\\resultados_bat.pdf", bbox_inches='tight')

fig, axs = plt.subplots(figsize=(fig_width_cm, fig_height_cm * 2), nrows=3, ncols=1, sharex=True)
i = 0
for file in files:
    df = pd.read_pickle(path + "\\" + file)
    # print(df)
    limiar = file.split("_")[1]
    axs[0].plot(df["Tempo"], df['SoC_UC'], linewidth = 2, color = colors[i], label = limiar.split(".")[0])
    axs[1].plot(df["Tempo"], df['v_banco_uc'], linewidth = 2, color = colors[i], label = limiar.split(".")[0])
    axs[2].plot(df["Tempo"], df['i_uc'], linewidth = 2, color = colors[i], label = limiar.split(".")[0])
    i += 1

axs[0].grid()
axs[0].set_ylabel(r"SoC [\%]", fontweight = 'bold')
axs[0].legend(loc='upper right')

axs[1].grid()
axs[1].set_ylabel("Tensão [V]", fontweight = 'bold')
axs[1].legend(loc='upper right')

axs[2].grid()
axs[2].set_ylabel("Corrente [A]", fontweight = 'bold')
axs[2].set_xlabel("Tempo [s]", fontweight = 'bold')
axs[2].set_xlim(df["Tempo"][0], df["Tempo"][len(df["Tempo"])-1])
axs[2].legend(loc='upper right')
plt.tight_layout()
plt.savefig("figuras\\resultados_UC.pdf", bbox_inches='tight')


fig, axs = plt.subplots(figsize=(fig_width_cm, fig_height_cm * 2), nrows=3, ncols=1, sharex=True)
i = 0
for file in files:
    df = pd.read_pickle(path + "\\" + file)
    # print(df)
    limiar = file.split("_")[1]
    axs[0].plot(df["Tempo"], df['p_bat_reject'], linewidth = 2, color = colors[i], label = limiar.split(".")[0])
    axs[1].plot(df["Tempo"], df['p_uc_reject'], linewidth = 2, color = colors[i], label = limiar.split(".")[0])
    axs[2].plot(df["Tempo"], df['p_reject'], linewidth = 2, color = colors[i], label = limiar.split(".")[0])
    i += 1

axs[0].grid()
axs[0].set_ylabel("Potência [kW]", fontweight = 'bold')
axs[0].set_title("Potência Rejeitada - Bateria", fontweight = 'bold')
axs[0].legend(loc='upper right')

axs[1].grid()
axs[1].set_ylabel("Potência [kW]", fontweight = 'bold')
axs[1].set_title("Potência Rejeitada - Supercapacitor", fontweight = 'bold')
axs[1].legend(loc='upper right')

axs[2].grid()
axs[2].set_ylabel("Potência [kW]", fontweight = 'bold')
axs[2].set_xlabel("Tempo [s]", fontweight = 'bold')
axs[2].set_xlim(df["Tempo"][0], df["Tempo"][len(df["Tempo"])-1])
axs[2].set_title("Potência Rejeitada - Total", fontweight = 'bold')
axs[2].legend(loc='upper right')
plt.tight_layout()
plt.savefig("figuras\\resultados_reject.pdf", bbox_inches='tight')

#Energia total do banco de baterias


plt.show()

    