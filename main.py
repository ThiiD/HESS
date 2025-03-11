import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
        """
        Configura parâmetros da bateria
        :param float C: Taxa de descarga da bateria (Ah)
        :param int Ns: Número de baterias em série
        :param int Np: Número de baterias em paralelo
        :param int Nm: Número de módulos
        :param float Vnom: Tensão nominal por célula (V)
        :param float SoC: Estado de carga inicial da bateria (%)
        :raises ValueError: Se os parâmetros forem inválidos
        """
        self._batt.setParams(C, Ns, Np, Nm, Vnom, SoC)

    def setParam_UC(self, C: float, Ns: int, Np: int, Nm : int, Vnom: float, SoC: float) -> None:
        """Configura parâmetros do supercapacitor
        :param float C: Capacitância do supercapacitor (F)
        :param int Ns: Número de supercapacitores em série
        :param int Np: Número de supercapacitores em paralelo
        :param int Nm: Número de módulos
        :param float Vnom: Tensão nominal do supercapacitor (V)
        :param float SoC: Estado de carga inicial do supercapacitor (%)
        """
        self._uc.setParams(C, Ns, Np, Nm, Vnom, SoC)

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

    def simulate(self, data: str, sheet: str, threshold : float) -> None:
        """Executa simulação
        :param str data: Caminho para arquivo de dados
        :param str sheet: Nome da planilha
        :param float threshold: Limiar de potência para distribuição (kW)
        """
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
            power_bat, power_uc = self.supervisory_control(power, threshold)
            
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
        print(self._SoC_UC)                                     # APAGAR DEPOIS
        self.plot_results(data["Time"])

    def supervisory_control(self, power: float, threshold : float) -> tuple[float, float]:
        """
        Estratégia de controle para distribuição de potência
        :param float power: Potência atual (kW)
        :param float threshold: Limiar de potência para distribuição (kW)
        """
        # Estratégia: UC absorve potências de pico
        power = power * 1000                                                        # Conversão para W
        threshold = threshold * 1000                                                # Conversão para W
        if abs(power) > threshold:                                                  
            power_uc = power - threshold if power > 0 else power + threshold
            power_bat = threshold if power > 0 else -threshold
        else:
            power_uc = 0
            power_bat = power
            
        return power_bat, power_uc

    def size_energy_storage(self, data: pd.DataFrame, threshold: float, config_bat : dict, config_uc : dict) -> tuple[dict, dict]:
        """
        Dimensiona banco de baterias e supercapacitores baseado no limiar de potência
        
        :param pd.DataFrame data: DataFrame com dados de potência
        :param float threshold: Limiar de potência para distribuição (kW)
        :param float config_bat: Configuração de tensão desejada (número de celulas serie e modulos)
        :param float config_uc: Configuração de tensão desejada (número de UC serie e modulos)
        :return: Dicionários com parâmetros da bateria e supercapacitor
        """
        # Converte threshold para W
        threshold = threshold * 1000
        
        # Calcula potências
        powers = (data['Traction Power'] - data["Braking Power"]) * 1000  # Converte para W
        
        # Separa potências entre bateria e UC
        power_bat = powers.copy()
        power_uc = powers.copy()
        
        # Aplica threshold
        power_bat[powers > threshold] = threshold
        power_bat[powers < -threshold] = -threshold
        power_uc[abs(powers) <= threshold] = 0
        power_uc[powers > threshold] = powers[powers > threshold] - threshold
        power_uc[powers < -threshold] = powers[powers < -threshold] + threshold
        
        # Calcula energias acumuladas
        dt = 1  # intervalo de 1s
        energy_bat = np.cumsum(power_bat * dt / 3600)  # Wh
        energy_uc = np.cumsum(power_uc * dt / 3600)    # Wh
        
        # Encontra máximas energias acumuladas
        max_energy_bat = np.max(np.abs(energy_bat))             
        max_energy_uc = np.max(np.abs(energy_uc))               
        
        # Aplicação fator de segurança
        n = 1.2
        max_energy_bat *= n
        max_energy_uc *= n


        # Dimensiona bateria
        Vnom_bat = 3.2  # V
        C_bat = 40       # Ah
        energy_cell_bat = Vnom_bat * C_bat  # Wh por célula
        
        # Número de células necessárias
        N_cells_bat = np.ceil(max_energy_bat / energy_cell_bat)
        
        # Configura arranjo (otimização básica)
        Ns_bat = config_bat["Ns"]
        Nm_bat = config_bat["Nm"]
        Np_bat = np.ceil(N_cells_bat / (Ns_bat * Nm_bat))
        
        
        # Dimensiona supercapacitor
        Vnom_uc = 3   # V
        C_uc = 3000     # F
        
        # Energia máxima por célula UC (E = 1/2 * C * V²)
        #energy_cell_uc = 0.5 * C_uc * (Vnom_uc**2) / 3600  # Wh

        # Configura arranjo (otimização básica)
        Ns_uc = config_uc["Ns"]                 # Fixo por restrições de tensão
        Nm_uc = config_uc["Nm"]

        # Calculo para numero de celulas em paralelo
        C_t = 2 * max_energy_uc/ ((Vnom_uc * Ns_uc * Nm_uc )**2)  # F
        Np_uc = np.ceil((C_t * Ns_uc * Nm_uc) / C_uc)

        if Np_uc < 3: # COndição para conseguir absorver a potencia de pico
            Np_uc = 3
        
        # Número de células necessárias
        #N_cells_uc = np.ceil(max_energy_uc / energy_cell_uc)
        
        
        #Np_uc = np.ceil(N_cells_uc / (Ns_uc * Nm_uc))
        
        
        # Retorna parâmetros calculados
        battery_params = {
            'C': C_bat,
            'Ns': int(Ns_bat),
            'Np': int(Np_bat),
            'Nm': int(Nm_bat),
            'Vnom': Vnom_bat,
            'max_energy': max_energy_bat
        }
        
        uc_params = {
            'C': C_uc,
            'Ns': int(Ns_uc),
            'Np': int(Np_uc),
            'Nm': int(Nm_uc),
            'Vnom': Vnom_uc,
            'max_energy': max_energy_uc
        }
        
        return battery_params, uc_params

if __name__ == "__main__":
    data = r"data\CR-3112_28-09-24_AGGREGATED.xlsx"
    sheet = "Dados"
    simulation = Simulation()
    
    # Carrega dados
    df = pd.read_excel(data, sheet_name=sheet)
    
    # Dimensiona componentes
    threshold = 1000  # 500 kW

    # Parâmetros da bateria para diferentes níveis de tensão
    voltage_configs_bat = {
        540: {"Ns": 16, "Nm": 10},   # 16 * 10 * 3.35 ≈ 540V
        720: {"Ns": 16, "Nm": 14},   # 16 * 13 * 3.35 ≈ 720V
        960: {"Ns": 16, "Nm": 18},   # 16 * 18 * 3.35 ≈ 960V
        1080: {"Ns": 16, "Nm": 20},  # 16 * 20 * 3.35 ≈ 1080V
        1260: {"Ns": 16, "Nm": 24},  # 16 * 24 * 3.35 ≈ 1260V
        1440: {"Ns": 16, "Nm": 27}   # 16 * 27 * 3.35 ≈ 1440V
    }

    # Seleciona configuração desejada
    target_voltage_bat = 1260  # Escolha uma das tensões válidas
    config_bat = voltage_configs_bat[target_voltage_bat]

    # Parâmetros do supercapacitor para diferentes níveis de tensão
    voltage_configs_uc = { 240 : {"Ns": 8, "Nm" : 10},  # 8 * 10 * 3.0 ≈ 240V
                           360 : {"Ns": 8, "Nm" : 15},  # 8 * 15 * 3.0 ≈ 360V
                           480 : {"Ns": 8, "Nm" : 20},  # 8 * 20 * 3.0 ≈ 480V
                           600 : {"Ns": 8, "Nm" : 25},  # 8 * 25 * 3.0 ≈ 600V
                           720 : {"Ns": 8, "Nm" : 30},  # 8 * 30 * 3.0 ≈ 720V
                        }   
    
    # Seleciona configuração desejada
    target_voltage_uc = 480  # Escolha uma das tensões válidas
    config_uc = voltage_configs_uc[target_voltage_uc]


    batt_params, uc_params = simulation.size_energy_storage(df, threshold, config_bat, config_uc)
    
    
    
    # Inicializa o SoC da bateria e do supercapacitor
    batt_params['SoC'] = 50
    uc_params['SoC'] = 20

    # # Parâmetros da bateria
    # C_bat = 40
    # Ns_bat = config_bat["Ns"]
    # Np_bat = 3
    # Nm = config_bat["Nm"]
    # Vnom_bat = 3.35
    # SoC = 50

    print(f"uc_params['Np'] : {uc_params['Np']}")
    # Configura componentes com parâmetros calculados
    simulation.setParam_Batt(
        C=batt_params['C'],
        Ns=batt_params['Ns'],
        Np=batt_params['Np'],
        Nm=batt_params['Nm'],
        Vnom=batt_params['Vnom'],
        SoC=batt_params['SoC']  
    )
    
    simulation.setParam_UC(
        C=uc_params['C'],
        Ns=uc_params['Ns'],
        Np=uc_params['Np'],
        Nm=uc_params['Nm'],
        Vnom=uc_params['Vnom'],
        SoC=uc_params['SoC']
    )

    # Prints para conferencia:
    print(f'batt_params: {batt_params}')
    print(f'uc_params: {uc_params}')
    
    # Executa simulação
    simulation.simulate(data, sheet, threshold)
    
    # Mostra resultados do dimensionamento
    print("\nResultados do dimensionamento:")
    print(f"\nBateria:")
    print(f"Energia máxima: {batt_params['max_energy']:.2f} Wh")
    print(f"Número de células: {batt_params['Ns']*batt_params['Np']*batt_params['Nm']}")
    print(f"Arranjo: {batt_params['Np']}P x {batt_params['Ns']}S x {batt_params['Nm']}M")
    
    print(f"\nSupercapacitor:")
    print(f"Energia máxima: {uc_params['max_energy']:.2f} Wh")
    print(f"Número de células: {uc_params['Ns']*uc_params['Np']*uc_params['Nm']}")
    print(f"Arranjo: {uc_params['Np']}P x {uc_params['Ns']}S x {uc_params['Nm']}M")
