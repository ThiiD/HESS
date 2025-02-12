import pandas as pd
import matplotlib.pyplot as plt
from batt import Batt
from UC import Uc

class Simulation():
    fig_width_cm = 24/2.4
    fig_height_cm = 18/2.4
    _SoC = []
    _v_banco = []
    _i_bat = []
    def __init__(self):
        """
        Método para calcular o fluxo de potência do caminhão.
        """
        self._uc = Uc()
        self._batt = Batt()



    def setParam_Batt(self, C : int, Ns : int, Np : int, Nm : int, Vnom : float,SoC : float) -> None:
        """
        :param int C: Taxa de descarga da bateria.
        :param int Ns: Número de baterias em serie.
        :param int Np: Número de baterias em paralelo.
        :param int Nm: Número de modulos.
        :param float Vnom: Tensão nominal da bateria.
        :param float SoC: SoC inicial da bateria
        """
        self._batt.setParams(C, Ns, Np, Nm, Vnom, SoC)

    def setParam_UC(self):
        pass
        

    def simulate(self, data : str, sheet : str) -> None:
        """
        :param str data: path para o arquivo .xslx
        """
        data = pd.read_excel(data, sheet_name= sheet)
        data["Time"] = range(0, len(data))
        powers = data['Traction Power'] - data["Braking Power"]
        print(data)

        fig, axs = plt.subplots(figsize = (self.fig_width_cm, self.fig_height_cm), nrows = 3, ncols = 1, sharex = True)
        axs[0].step(data["Time"], data["Traction Power"], where="post", linewidth = 2, color = "tab:blue", label = "Traction")
        axs[0].grid()
        axs[0].legend(loc="upper right")
        axs[0].set_ylabel("Potência [kWh]")


        axs[1].step(data["Time"], data["Braking Power"], where="post", linewidth = 2, color = "tab:orange", label = "Braking")
        axs[1].grid()
        axs[1].legend(loc="upper right")
        axs[1].set_ylabel("Potência [kWh]")
        

        
        axs[2].step(data["Time"], powers, where="post", linewidth = 2, color = "tab:green", label = "Power")
        axs[2].grid()
        axs[2].set_ylabel("Potência [kWh]")
        axs[2].legend(loc="upper right")
        axs[2].set_xlim(0, data["Time"].iloc[-1])

        plt.tight_layout()
        plt.show(block = False)

        
        for power in powers:
            power_bat, power_uc = self.supervisory_control(power)
            i_bat = self._batt.setCurrent(power_bat)
            self._i_bat.append(i_bat)
            SoC, v_banco = self._batt.updateEnergy(i_bat, 1)
            self._SoC.append(SoC)
            self._v_banco.append(v_banco)


        fig, axs = plt.subplots(figsize = (self.fig_width_cm, self.fig_height_cm), nrows = 3, ncols=1, sharex=True)
        axs[0].plot(data["Time"], self._SoC, color = "tab:blue", label = "SoC")
        axs[0].grid()
        axs[0].legend(loc="upper right")
        axs[0].set_ylabel("SoC [%]")

        axs[1].plot(data["Time"], self._v_banco, color = "tab:orange", label = "Tensão")
        axs[1].grid()
        axs[1].legend(loc="upper right")
        axs[1].set_ylabel("Tensão [V]")

        axs[2].plot(data["Time"], self._i_bat, color = "tab:green", label = "Corrente")
        axs[2].grid()
        axs[2].legend(loc="upper right")
        axs[2].set_ylabel("Corrente [A]")
        axs[2].set_xlim(0, data["Time"].iloc[-1])
        plt.show()

    
    def supervisory_control(self, power : int) -> tuple:
        """
        Método para calcular a distribuição de potencia entre bateria e supercapacitor
        :param int power: Potencia instantanea.
        """
        
        power_bat = power
        power_uc = 0

        return power_bat, power_uc
        




if __name__ == "__main__":
    C = 40
    Ns = 16
    Np = 3
    Nm = 24
    Vnom = 3.35
    SoC = 50

    data = r"data\CR-3112_28-09-24_AGGREGATED.xlsx"
    sheet = "Dados"
    simulation = Simulation()
    simulation.setParam_Batt(C, Ns, Np, Nm, Vnom, SoC)
    simulation.simulate(data, sheet)
