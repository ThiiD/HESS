import numpy as np
from time import sleep

class Uc():
    def __init__(self):
        """Inicializa um banco de supercapacitores com valores padrão"""
        self._C = 3140                                                                  # Capacitância em Farads
        self._Ns = 40                                                                   # Número de capacitores em série
        self._Np = 10                                                                   # Número de strings em paralelo
        self._Nm = 5                                                                    # Número de módulos em serie
        self._v_cap = 3                                                                 # Tensão atual do capacitor
        
        self._SoC_max = 100                                                             # SoC máximo permitido (%)
        self._SoC_min = 3                                                               # SoC mínimo permitido (%)

        self._v_total = self._v_cap * self._Ns * self._Nm                               # Tensão total do banco
        self._min_v = (self._SoC_min / 100) * self._v_cap * self._Ns * self._Nm         # Tensão mínima (30% Vnom)
        self._max_v = (self._SoC_max / 100 ) * self._v_cap * self._Ns * self._Nm        # Tensão máxima
        self._v_banco = self._v_cap * self._Ns * self._Nm                               # Tensão total do banco
        self._total_energy = 0.5 * (self._C * self._Np/(self._Ns * self._Nm)) * (self._v_banco**2)   # Energia em Joules

        self._SoC = 50                                                                  # Estado de carga inicial (%)
        self._stored_energy = self.soc2energy(self._SoC)                                # Energia atual armazenada        
        self._v_atual = self.energy2voltage(self._stored_energy)                        # Tensão atual do banco

    def setParams(self, C: float, Ns: int, Np: int, Nm : int, Vnom: float, SoC: float) -> None:
        """e
        Configura os parâmetros do banco de supercapacitores
        :param float C: Capacitância por célula (F)
        :param int Ns: Número de capacitores em série
        :param int Np: Número de strings em paralelo
        :param int Nm: Número de módulos em série
        :param float Vnom: Tensão nominal por célula (V)
        :param float SoC: Estado de carga inicial do banco (%)
        :raises ValueError: Se os parâmetros forem inválidos
        """
        if any(x <= 0 for x in [C, Ns, Np, Nm,  Vnom, SoC]):
            raise ValueError("Todos os parâmetros devem ser positivos")

        self._C = C
        self._Ns = Ns
        self._Np = Np
        self._Nm = Nm
        self._Vnom = Vnom
        self._SoC = SoC
        self._v_banco = Vnom * self._Ns * self._Nm * (self._SoC / 100)
        self._v_cap = self._v_banco / (self._Ns * self._Nm)

        self._min_v = 0.05 * Vnom
        self._max_v = Vnom
        self._total_energy = 0.5 * (C * Np/(Ns * Nm)) * (self._v_banco**2)             # Energia total que pode ser armazenada no banco
        self._stored_energy = self.soc2energy(SoC)                              # Energia atual armazenada

    def energy2soc(self, energy: float) -> float:
        """
        Calcula SoC baseado na energia armazenada no banco de UC.
        :param float energy: Energia armazenada (J)
        :return float: Estado de carga do banco (%)
        """
        return (energy / self._total_energy) * 100

    def soc2energy(self, SoC: float) -> float:
        """
        Calcula energia armazenada no banco de UC baseada no SoC.
        :param float SoC: Estado de carga do banco (%)
        :return float: Energia armazenada (J)
        """
        return (SoC/100) * self._total_energy

    def voltage2energy(self, voltage: float) -> float:
        """
        Calcula energia armazenada no banco de UC baseada na tensão.
        :param float voltage: Tensão do banco (V)
        :return float: Energia armazenada (J)
        """
        return 0.5 * (self._C * self._Np/(self._Ns * self._Nm)) * (voltage**2)
    
        # equação que converte um banco de ultracapacitores com Np strings em paralelo, Ns ultracapacitores em série e Nm módulos em série para energia armazenada em Joules
        # E = 0.5 * C * Np/Ns * V^2

    def energy2voltage(self, energy: float) -> float:
        """
        Calcula tensão baseada na energia armazenada no banco de UC.
        :param float energy: Energia armazenada (J)
        :return float: Tensão do banco (V)
        """
        return np.sqrt((2 * energy) / (self._C * self._Np/(self._Ns * self._Nm)))

    def setCurrent(self, power: float) -> float:
        """
        Calcula corrente baseada na potência requerida
        :param float power: Potência requerida (W)
        :return float: Corrente (A)
        """
        i = power / self._v_banco
        i_max = 280 * self._Np                                      # Corrente maxima no banco de UC
        return np.clip(i, -i_max, i_max)

    def updateEnergy(self, current: float, dt: float) -> tuple[float, float]:
        """
        Atualiza energia do banco usando a corrente
        :param float current: Corrente do banco (A, + carga, - descarga)
        :param float dt: Intervalo de tempo (s)
        :return tuple[float, float]: (Tensão do banco, Energia armazenada)
        """
        # Calcula variação de energia (P = V*I)
        energy_variation = -1 * self._v_banco * current * dt
        print(f'energy_variation: {energy_variation}')
        
        # Atualiza energia armazenada
        new_energy = self._stored_energy + energy_variation
        print(f'new_energy: {new_energy}')
        
        # Limita energia entre mínimo e máximo
        min_energy = self.voltage2energy(self._min_v * self._Ns * self._Nm)
        max_energy = self.voltage2energy(self._max_v * self._Ns * self._Nm)
        new_energy = np.clip(new_energy, min_energy, max_energy)
        print(f'min_energy: {min_energy}')
        print(f'max_energy: {max_energy}')
        print(f'new_energy_clipped: {new_energy}')
        
        # Atualiza estados
        self._stored_energy = new_energy
        self._v_banco = self.energy2voltage(new_energy)
        print(f'v_banco: {self._v_banco}')

        self._v_cap = self._v_banco / self._Ns
        self._SoC = self.energy2soc(new_energy)
        print(f'SoC: {self._SoC}')
        #sleep(2)
        print("-----------------------------------------")
        
        return self._SoC, self._v_banco