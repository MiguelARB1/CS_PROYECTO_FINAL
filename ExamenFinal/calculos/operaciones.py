
def calcular_bonificaciones_descuentos(sueldo_base,horas_extra,dias_falta,minutos_falta):

    pagoHorasExtras = 1.50 * horas_extra*sueldo_base / 30 / 8
    movilidad = 1000
    bonificacionSuplementaria = 0.03 * sueldo_base
    bonificaciones = round(movilidad + bonificacionSuplementaria+ pagoHorasExtras,2)
    remuneracionComputable = sueldo_base + movilidad+ bonificacionSuplementaria
    remuneracionMinima = sueldo_base + bonificaciones
    DescuentoFaltas = remuneracionComputable / 30 * dias_falta
    descuentoTardanzas = remuneracionComputable / 30 / 8 / 60* minutos_falta
    descuentos = round(DescuentoFaltas + descuentoTardanzas,2)
    return bonificaciones ,descuentos