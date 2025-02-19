import pandas as pd
import matplotlib.pyplot as plt
from batt import Batt
from UC import Uc

class Simulation():
    def __init__(self):
        """Método para calcular o fluxo de potência do caminhão."""
        self.fig_width_cm = 24/2.4
        self.fig_height_cm = 18/2.4
        
        # Dados da bateria
        self._SoC = []
        self._v_banco_bat = []
        self._i_bat = []
        
        # Dados do supercapacitor
        self._v_banco_uc = []
        self._i_uc = []
        self._SoC_UC = []
        
        self._uc = Uc()
        self._batt = Batt()

    def setParam_Batt(self, C: float, Ns: int, Np: int, Nm: int, Vnom: float, SoC: float) -> None:
        """Configura parâmetros da bateria"""
        self._batt.setParams(C, Ns, Np, Nm, Vnom, SoC)

    def setParam_UC(self, C: float, Ns: int, Np: int, Vnom: float, v_init: float) -> None:
        """Configura parâmetros do supercapacitor"""
        self._uc.setParams(C, Ns, Np, Vnom, v_init)

    def plot_power_distribution(self, data, powers):
        """Plota distribuição de potência"""
        fig, axs = plt.subplots(figsize=(self.fig_width_cm, self.fig_height_cm), nrows=3, ncols=1, sharex=True)
        
        axs[0].step(data["Time"], data["Traction Power"], where="post", linewidth=2, color="tab:blue", label="Tração")
        axs[0].grid()
        axs[0].legend(loc="upper right")
        axs[0].set_ylabel("Potência [kW]")

        axs[1].step(data["Time"], data["Braking Power"], where="post", linewidth=2, color="tab:orange", label="Frenagem")
        axs[1].grid()
        axs[1].legend(loc="upper right")
        axs[1].set_ylabel("Potência [kW]")

        axs[2].step(data["Time"], powers, where="post", linewidth=2, color="tab:green", label="Total")
        axs[2].grid()
        axs[2].set_ylabel("Potência [kW]")
        axs[2].legend(loc="upper right")
        axs[2].set_xlim(0, data["Time"].iloc[-1])
        
        plt.tight_layout()
        plt.show(block=False)

    def plot_LUT(self):
        """Plota LUT da bateria"""
        df = pd.read_csv("data\\LUT_batt.csv", sep=";")
        plt.figure(figsize=(self.fig_width_cm, self.fig_height_cm/2))
        plt.plot(100 - df["SoC"], df["Tensao"], color = 'tab:blue', linewidth = 2, label = "LUT Bateria")   
        plt.grid()
        plt.legend(loc="upper left")
        plt.ylabel("Tensão [V]")
        plt.xlabel("SoC [%]")
        plt.title("Curva SoC x Tensão da bateria")
        plt.xlim(0, 100)
        plt.show(block = False)

    def plot_results(self, time):
        """Plota resultados da simulação"""
        fig, axs = plt.subplots(3, 2, figsize=(self.fig_width_cm*2, self.fig_height_cm), sharex=True)
        
        # Bateria (coluna esquerda)
        axs[0,0].step(time, self._SoC, linewidth=2, color="tab:blue", label="SoC Bateria")
        axs[0,0].grid()
        axs[0,0].legend(loc="upper right")
        axs[0,0].set_ylabel("SoC [%]")

        axs[1,0].step(time, self._v_banco_bat, linewidth=2, color="tab:orange", label="Tensão Bateria")
        axs[1,0].grid()
        axs[1,0].legend(loc="upper right")
        axs[1,0].set_ylabel("Tensão [V]")

        axs[2,0].step(time, self._i_bat, linewidth=2, color="tab:green", label="Corrente Bateria")
        axs[2,0].grid()
        axs[2,0].legend(loc="upper right")
        axs[2,0].set_ylabel("Corrente [A]")
        axs[2,0].set_xlabel("Tempo [s]")
        axs[2,0].set_xlim(0, time.iloc[-1])
        
        # Supercapacitor (coluna direita)
        axs[0,1].step(time, self._SoC_UC, linewidth=2, color="tab:blue", label="SoC UC")
        axs[0,1].grid()
        axs[0,1].legend(loc="upper right")
        axs[0,1].set_ylabel("SoC [%]")

        axs[1,1].step(time, self._v_banco_uc, linewidth=2, color="tab:orange", label="Tensão UC")
        axs[1,1].grid()
        axs[1,1].legend(loc="upper right")
        axs[1,1].set_ylabel("Tensão [V]")

        axs[2,1].step(time, self._i_uc, linewidth=2, color="tab:green", label="Corrente UC")
        axs[2,1].grid()
        axs[2,1].legend(loc="upper right")
        axs[2,1].set_ylabel("Corrente [A]")
        axs[2,1].set_xlabel("Tempo [s]")
        axs[2,1].set_xlim(0, time.iloc[-1])
        
        plt.tight_layout()
        plt.show()

    def simulate(self, data: str, sheet: str) -> None:
        """Executa simulação"""
        data = pd.read_excel(data, sheet_name=sheet)
        data["Time"] = range(0, len(data))
        powers = data['Traction Power'] - data["Braking Power"]
        
        # Plota distribuição de potência
        self.plot_power_distribution(data, powers)
        # Plota LUT bateria
        self.plot_LUT()
        
        # Simulação
        for power in powers:
            # Distribuição de potência
            power_bat, power_uc = self.supervisory_control(power)
            
            # Atualiza bateria
            i_bat = self._batt.setCurrent(power_bat)
            SoC, v_banco_bat = self._batt.updateEnergy(i_bat, 1)
            
            # Atualiza supercapacitor
            i_uc = self._uc.setCurrent(power_uc)
            SoC_uc, v_banco_uc = self._uc.updateEnergy(i_uc, 1)
            
            # Armazena resultados
            self._SoC.append(SoC)
            self._v_banco_bat.append(v_banco_bat)
            self._i_bat.append(i_bat)
            self._SoC_UC.append(SoC_uc)
            self._i_uc.append(i_uc)
            self._v_banco_uc.append(v_banco_uc)

        # Plota resultados
        self.plot_results(data["Time"])

    def supervisory_control(self, power: float) -> tuple[float, float]:
        """Estratégia de controle para distribuição de potência"""
        # Estratégia: UC absorve potências de pico
        power = power * 1000                            # Conversão para W
        threshold = 1000 * 1000                         # 5MW
        if abs(power) > threshold:                        # 1000MW
            power_uc = power - threshold if power > 0 else power + threshold
            power_bat = threshold if power > 0 else -threshold
        else:
            power_uc = 0
            power_bat = power
            
        return power_bat, power_uc

if __name__ == "__main__":
    # Parâmetros da bateria
    C_bat = 40
    Ns_bat = 16
    Np_bat = 3
    Nm = 24
    Vnom_bat = 3.35
    SoC = 50

    # Parâmetros do supercapacitor
    C_uc = 3000
    Ns_uc = 200
    Np_uc = 10
    Vnom_uc = 2.7
    v_init = 2.7

    data = r"data\CR-3112_28-09-24_AGGREGATED.xlsx"
    sheet = "Dados"
    simulation = Simulation()
    
    # Configura componentes
    # simulation.setParam_Batt(C_bat, Ns_bat, Np_bat, Nm, Vnom_bat, SoC)
    # simulation.setParam_UC(C_uc, Ns_uc, Np_uc, Vnom_uc, v_init)
    
    # Executa simulação
    simulation.simulate(data, sheet)
