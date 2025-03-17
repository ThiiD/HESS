import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import tabulate

params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern',
          'axes.labelweight' : 'bold'
          }
plt.rcParams.update(params)

fig_width_cm = 8/1.4
fig_height_cm = 3.54/1.4

data_path= r'data\CR-3112_28-09-24_AGGREGATED.xlsx'
df = pd.read_excel(data_path, sheet_name = "Log")
df2 = pd.read_excel(data_path, sheet_name = "Dados")

# print(df["Time"][0])
# print(type(df["Time"][0]))
# # print(df["Time"])
# # df['Time'] = pd.to_datetime(df['Time'], format='%d/%m/%Y %H:%M:%S')
# df["Time"] = df["Time"].dt.strftime('%H:%M:%S')
# print(df["Time"][0])
# print(type(df["Time"][0]))

# Formatação do eixo X



fig, axs = plt.subplots(figsize=(fig_width_cm, fig_height_cm * 1.5), nrows=2, ncols=1, sharex=True)
axs[0].plot(df["Time"], df['fa00_altoutvolts'], linewidth = 2, color = 'tab:blue', label = "Tensão")
axs[0].grid()
axs[0].set_ylabel("Tensão [V]", fontweight = 'bold')
axs[0].legend(loc='upper right')


axs[1].plot(df["Time"], df['fa08_m2amps'], linewidth = 2, color = 'tab:orange', label = "Corrente")
axs[1].grid()
axs[1].set_xlim([df["Time"][0], df["Time"][len(df["Time"])-1]])
axs[1].set_ylabel("Corrente [A]", fontweight = 'bold')
axs[1].set_xlabel("Horário", fontweight = 'bold')

axs[1].legend(loc='upper right')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()
plt.savefig("figuras\\perfil_de_tensao.pdf", bbox_inches='tight')
# plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))  # Ajuste o intervalo conforme necessário
# plt.gcf().autofmt_xdate()  # Rotacionar labels do eixo X para melhor leitura


plt.figure(figsize=(fig_width_cm, fig_height_cm))

threshold = 1000
plt.plot(df["Time"], df2["Traction Power"] - df2["Braking Power"], linewidth = 2, color = 'tab:green', label = "Potência Total")
plt.text(df["Time"].iloc[len(df)//2 + 100], threshold + 50, 'Limiar de Potência', color='red', fontweight='bold', horizontalalignment='right')
plt.hlines(threshold, df["Time"][0], df["Time"].iloc[-1], color = 'tab:red', linestyle = '--')
plt.hlines(-1 * threshold, df["Time"][0], df["Time"].iloc[-1], color = 'tab:red', linestyle = '--')
plt.text(df["Time"].iloc[len(df)//2 + 150], -1* (threshold) - 310, 'Limiar de Potência', color='red', fontweight='bold', horizontalalignment='right')
plt.grid()
plt.ylabel("Potência [kW]", fontweight = 'bold')
plt.xlabel("Horário", fontweight = 'bold')
plt.xlim([df["Time"][0], df["Time"][len(df["Time"])-1]])
plt.legend(loc='lower left')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.savefig("figuras\\perfil_de_potencia.pdf", bbox_inches='tight')
plt.show()


# ----------------------------------------------------------
# ------------------- Dados de Operação --------------------
# ----------------------------------------------------------

energia_requerida_total = df2["Traction Energy"].sum()
energia_gerada_total = df2["Braking Energy"].sum()
potencia_maxima = df2["Traction Power"].max()
potencia_minima = df2["Braking Power"].max()
# fazer uma column para fa00_altoutvolts para quando fa08_m2amps for maior que 0:
tensao_tracao = df['fa00_altoutvolts'][df['fa08_m2amps'] > 0]
tensao_frenagem = df['fa00_altoutvolts'][df['fa08_m2amps'] < 0]
tensao_tracao_maxmima = tensao_tracao.max()
tensao_frenagem_maxima = tensao_frenagem.max()
corrente_maxima_requerida = df['fa08_m2amps'].max()
corrente_minima_requerida = df['fa08_m2amps'].min()

print(tabulate.tabulate([["Energia Requerida Total [kWh]", energia_requerida_total],
                         ["Energia Gerada Total [kWh]", energia_gerada_total],
                         ["Potência Máxima [kW]", potencia_maxima],
                         ["Potência Mínima [kW]", potencia_minima],
                         ["Tensão Máxima de Tração [V]", tensao_tracao_maxmima],
                         ["Tensão Máxima de Frenagem [V]", tensao_frenagem_maxima],
                         ["Corrente Máxima Requerida [A]", corrente_maxima_requerida],
                         ["Corrente Mínima Requerida [A]", corrente_minima_requerida]], tablefmt='fancy_grid'))     
