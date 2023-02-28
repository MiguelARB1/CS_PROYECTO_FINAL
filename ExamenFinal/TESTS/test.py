import unittest
from calculos.operaciones import calcular_bonificaciones_descuentos

class TestCalcularBonificacionesDescuentos(unittest.TestCase):

    def test_calculo_bonificaciones_descuentos(self):
        sueldo_base = 3000
        dias_falta = 1
        minutos_falta = 15
        horas_extra = 5
        bonificaciones_esperadas = 1183.75
        descuentos_esperados = 140.59

        bonificaciones, descuentos = calcular_bonificaciones_descuentos(sueldo_base, horas_extra, dias_falta, minutos_falta)

        self.assertEqual(bonificaciones, bonificaciones_esperadas)
        self.assertEqual(descuentos, descuentos_esperados)