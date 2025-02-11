import pandas as pd
import matplotlib.pyplot as plt
from batt import Batt
from UC import Uc

class Simulation():
    fig_width_cm = 24/2.4
    fig_height_cm = 18/2.4
    def __init__(self):
        """
        Método para calcular o fluxo de potência do caminhão.
        """
        self._uc = Uc()
        self._batt = Batt()



    def setParam_Batt(self, C, Ns, Np, Nm):
        """
        :param int C: Taxa de descarga da bateria.
        :param int Ns: Número de baterias em serie.
        :param int Np: Número de baterias em paralelo.
        :param int Nm: Número de modulos.
        """

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
            self._batt.setCurrent(power_bat)
            pass

    
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

    data = r"data\CR-3112_28-09-24_AGGREGATED.xlsx"
    sheet = "Dados"
    simulation = Simulation()
    simulation.simulate(data, sheet)
