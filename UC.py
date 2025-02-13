import numpy as np

class Uc():
    def __init__(self):
        """Inicializa um banco de supercapacitores com valores padrão"""
        self._C = 3000  # Capacitância em Farads
        self._Ns = 200  # Número de capacitores em série
        self._Np = 10   # Número de strings em paralelo
        self._Vnom = 2.7  # Tensão nominal (V)
        self._v_cap = self._Vnom  # Tensão atual do capacitor
        self._v_banco = self._v_cap * self._Ns  # Tensão total do banco
        self._min_v = 0.5 * self._Vnom  # Tensão mínima (50% Vnom)
        self._max_v = self._Vnom  # Tensão máxima
        self._total_energy = 0.5 * (self._C * self._Np/self._Ns) * (self._v_banco**2)  # Energia em Joules
        self._stored_energy = self._total_energy  # Energia atual armazenada

    def setParams(self, C: float, Ns: int, Np: int, Vnom: float, v_init: float) -> None:
        """
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

    def voltage2energy(self, voltage: float) -> float:
        """
        Calcula energia armazenada baseada na tensão
        :param float voltage: Tensão do banco (V)
        :return float: Energia armazenada (J)
        """
        return 0.5 * (self._C * self._Np/self._Ns) * (voltage**2)

    def energy2voltage(self, energy: float) -> float:
        """
        Calcula tensão baseada na energia armazenada
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
        i = (power * 1000) / self._v_banco
        i_max = 280 * self._Np  # Limite de corrente típico para supercapacitores
        return np.clip(i, -i_max, i_max)

    def updateEnergy(self, current: float, dt: float) -> tuple[float, float]:
        """
        Atualiza energia do banco usando a corrente
        :param float current: Corrente do banco (A, + carga, - descarga)
        :param float dt: Intervalo de tempo (s)
        :return tuple[float, float]: (Tensão do banco, Energia armazenada)
        """
        # Calcula variação de energia (P = V*I)
        energy_variation = self._v_banco * current * dt
        
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
        
        return self._v_banco, self._stored_energy