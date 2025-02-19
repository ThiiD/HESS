import numpy as np

class Uc():
    def __init__(self):
        """Inicializa um banco de supercapacitores com valores padrão"""
        self._C = 3140                                                                  # Capacitância em Farads
        self._Ns = 40                                                                   # Número de capacitores em série
        self._Np = 10                                                                   # Número de strings em paralelo
        self._Nm = 5                                                                    # Número de módulos em serie
        self._v_cap = 3                                                                 # Tensão atual do capacitor
        
        self._SoC_max = 100                                                             # SoC máximo permitido (%)
        self._SoC_min = 0                                                              # SoC mínimo permitido (%)

        self._v_total = self._v_cap * self._Ns * self._Nm                               # Tensão total do banco
        self._min_v = (self._SoC_min / 100) * self._v_cap * self._Ns * self._Nm         # Tensão mínima (30% Vnom)
        self._max_v = (self._SoC_max / 100 ) * self._v_cap * self._Ns * self._Nm        # Tensão máxima
        self._v_banco = self._v_cap * self._Ns * self._Nm                               # Tensão total do banco
        self._total_energy = 0.5 * (self._C * self._Np/self._Ns) * (self._v_banco**2)   # Energia em Joules

        self._SoC = 50                                                                  # Estado de carga inicial (%)
        self._stored_energy = self.soc2energy(self._SoC)                                # Energia atual armazenada        
        self._v_atual = self.energy2voltage(self._stored_energy)                        # Tensão atual do banco

    def setParams(self, C: float, Ns: int, Np: int, Vnom: float, v_init: float) -> None:
        """e
        Configura os parâmetros do banco de supercapacitores
        :param float C: Capacitância por célula (F)
        :param int Ns: Número de capacitores em série
        :param int Np: Número de strings em paralelo
        :param float Vnom: Tensão nominal por célula (V)
        :param float v_init: Tensão inicial por célula (V)
        :raises ValueError: Se os parâmetros forem inválidos
        """
        if any(x <= 0 for x in [C, Ns, Np, Vnom]):
            raise ValueError("Todos os parâmetros devem ser positivos")
        
        if not (0.5 * Vnom) <= v_init <= Vnom:
            raise ValueError(f"Tensão inicial deve estar entre {0.5*Vnom}V e {Vnom}V")

        self._C = C
        self._Ns = Ns
        self._Np = Np
        self._Vnom = Vnom
        self._v_cap = v_init
        self._v_banco = v_init * Ns
        self._min_v = 0.5 * Vnom
        self._max_v = Vnom
        self._total_energy = 0.5 * (C * Np/Ns) * (self._v_banco**2)
        self._stored_energy = self._total_energy

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
        return 0.5 * (self._C * self._Np/self._Ns) * (voltage**2)

    def energy2voltage(self, energy: float) -> float:
        """
        Calcula tensão baseada na energia armazenada no banco de UC.
        :param float energy: Energia armazenada (J)
        :return float: Tensão do banco (V)
        """
        return np.sqrt((2 * energy) / (self._C * self._Np/self._Ns))

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
        
        # Atualiza energia armazenada
        new_energy = self._stored_energy + energy_variation
        
        # Limita energia entre mínimo e máximo
        min_energy = self.voltage2energy(self._min_v * self._Ns)
        max_energy = self.voltage2energy(self._max_v * self._Ns)
        new_energy = np.clip(new_energy, min_energy, max_energy)
        
        # Atualiza estados
        self._stored_energy = new_energy
        self._v_banco = self.energy2voltage(new_energy)
        self._v_cap = self._v_banco / self._Ns
        self._SoC = self.energy2soc(new_energy)
        
        return self._SoC, self._v_banco