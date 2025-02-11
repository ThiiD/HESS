

class Batt():
    def __init__(self,):
        """
        
        """

    def setParam(self, C : int, Ns : int, Np : int, Nm : int, Vnom : int, v_banco : int, SoC : int) -> None:
        """
        :param int C: Taxa de descarga da bateria.
        :param int Ns: Número de baterias em serie.
        :param int Np: Número de baterias em paralelo.
        :param int Nm: Número de modulos.
        :param float Vnom: tensão nominal por celula. 
        :param float v_banco: tensão inicial do banco.
        :param float SoC: State of Charge inicial da bateria.
        """
        self._C = C
        self._Ns = Ns
        self._Np = Np
        self._Nm = Nm
        self._Vnom = Vnom
        self._v_banco = v_banco
        self._SoC = SoC

        self._total_energy = (Np * C) * (Ns * Nm * Vnom)
        self._SoC_Energy = SoC * self._total_energy
        

    def setCurrent(self, power):
        i = power / self._v_banco
        ic = i /self._Np


        
        if ic > 6 * self._C:
            i_out = 6 * self._C

        pass