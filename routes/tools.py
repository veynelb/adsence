from flask import Blueprint, render_template,request

tools_bp = Blueprint('tools', __name__)

@tools_bp.route('/calculadora-itbis', methods=['GET'])
def calculadora_itbis():
    return render_template('tools/calculadora_itbis.html')

@tools_bp.route('/usd-dop', methods=['GET'])
def usd_dop():
    tasa_actual = 61.20 
    return render_template('tools/usd_dop.html', tasa=tasa_actual)

@tools_bp.route('/generador-qr', methods=['GET'])
def generador_qr(): 
    return render_template('tools/generador_qr.html')

@tools_bp.route('/jpg-a-pdf', methods=['GET'])
def jpg_a_pdf(): 
    return render_template('tools/jpg_a_pdf.html')

@tools_bp.route('/sueldo-neto', methods=['GET', 'POST'])
def sueldo_neto():
    resultado = None
    sueldo_bruto = 0

    if request.method == 'POST':
        try:
            sueldo_bruto = float(request.form.get('sueldo_bruto', 0))
        except ValueError:
            sueldo_bruto = 0

        if sueldo_bruto > 0:
            # 1. Calcular Descuentos de TSS
            # Topes aproximados para 2026 basados en el salario mínimo del sector privado no sectorizado
            salario_minimo = 19300.00 
            tope_sfs = salario_minimo * 10
            tope_afp = salario_minimo * 20

            descuento_sfs = min(sueldo_bruto, tope_sfs) * 0.0304
            descuento_afp = min(sueldo_bruto, tope_afp) * 0.0287
            total_tss = descuento_sfs + descuento_afp

            # El ISR se calcula sobre el sueldo bruto MENOS la TSS
            sueldo_cotizable_mensual = sueldo_bruto - total_tss
            sueldo_cotizable_anual = sueldo_cotizable_mensual * 12

            # 2. Calcular Escala del ISR (DGII 2026)
            isr_anual = 0
            if sueldo_cotizable_anual <= 416220.00:
                isr_anual = 0
            elif sueldo_cotizable_anual <= 624329.00:
                isr_anual = (sueldo_cotizable_anual - 416220.00) * 0.15
            elif sueldo_cotizable_anual <= 867123.00:
                isr_anual = 31216.00 + ((sueldo_cotizable_anual - 624329.00) * 0.20)
            else:
                isr_anual = 79776.00 + ((sueldo_cotizable_anual - 867123.01) * 0.25)

            descuento_isr = isr_anual / 12
            sueldo_neto_mensual = sueldo_cotizable_mensual - descuento_isr

            resultado = {
                "bruto": round(sueldo_bruto, 2),
                "sfs": round(descuento_sfs, 2),
                "afp": round(descuento_afp, 2),
                "isr": round(descuento_isr, 2),
                "total_descuentos": round(total_tss + descuento_isr, 2),
                "neto_mensual": round(sueldo_neto_mensual, 2),
                "neto_quincenal": round(sueldo_neto_mensual / 2, 2)
            }

    return render_template('tools/sueldo_neto.html', resultado=resultado, sueldo_bruto=sueldo_bruto)

@tools_bp.route('/prestaciones-laborales', methods=['GET', 'POST'])
def prestaciones_laborales():
    resultado = None
    sueldo = 0
    meses_trabajados = 0

    if request.method == 'POST':
        try:
            sueldo = float(request.form.get('sueldo', 0))
            meses_trabajados = int(request.form.get('meses', 0))
            incluye_preaviso = request.form.get('preaviso') == 'si'
            incluye_vacaciones = request.form.get('vacaciones') == 'si'
        except ValueError:
            sueldo = 0
            meses_trabajados = 0

        if sueldo > 0 and meses_trabajados > 0:
            # Factor legal en RD para obtener el salario diario
            salario_diario = sueldo / 23.83
            
            # Calcular años completos y meses restantes
            anos = meses_trabajados // 12
            meses_restantes = meses_trabajados % 12

            # 1. Cálculo de Preaviso (Si aplica)
            dias_preaviso = 0
            if incluye_preaviso:
                if 3 <= meses_trabajados < 6:
                    dias_preaviso = 7
                elif 6 <= meses_trabajados < 12:
                    dias_preaviso = 14
                elif meses_trabajados >= 12:
                    dias_preaviso = 28
            monto_preaviso = dias_preaviso * salario_diario

            # 2. Cálculo de Cesantía
            dias_cesantias = 0
            # Días por meses sueltos o contratos de menos de un año
            if 3 <= meses_trabajados < 6:
                dias_cesantias = 6
            elif 6 <= meses_trabajados < 12:
                dias_cesantias = 13
            # Si tiene más de un año, se calcula por año acumulado
            elif meses_trabajados >= 12:
                if 1 <= anos < 5:
                    dias_cesantias = anos * 21
                else:
                    dias_cesantias = anos * 23
                
                # Proporción de meses del último año
                if 3 <= meses_restantes < 6:
                    dias_cesantias += 6
                elif 6 <= meses_restantes < 12:
                    dias_cesantias += 13

            monto_cesantias = dias_cesantias * salario_diario

            # 3. Vacaciones No Tomadas (Si aplica)
            dias_vacaciones = 0
            if incluye_vacaciones:
                if 5 <= meses_restantes < 6: # proporción del último año o si lleva menos de un año
                    dias_vacaciones = 6
                elif 6 <= meses_restantes < 7:
                    dias_vacaciones = 7
                elif 7 <= meses_restantes < 8:
                    dias_vacaciones = 8
                elif 8 <= meses_restantes < 9:
                    dias_vacaciones = 9
                elif 9 <= meses_restantes < 10:
                    dias_vacaciones = 10
                elif 10 <= meses_restantes < 11:
                    dias_vacaciones = 11
                elif meses_restantes >= 11 or (anos >= 1 and meses_restantes == 0):
                    dias_vacaciones = 14
            monto_vacaciones = dias_vacaciones * salario_diario

            # 4. Salario de Navidad Proporcional (Estimando salida a mitad de año promedio, 6 meses)
            # Para ser exactos de forma simple, tomamos los meses acumulados en el año actual (máximo 12)
            meses_ano_actual = meses_restantes if anos >= 1 else meses_trabajados
            if meses_ano_actual == 0: meses_ano_actual = 12 # Año completo cerrado
            monto_navidad = (sueldo * meses_ano_actual) / 12

            total_liquidisacion = monto_preaviso + monto_cesantias + monto_vacaciones + monto_navidad

            resultado = {
                "salario_diario": round(salario_diario, 2),
                "dias_preaviso": dias_preaviso,
                "monto_preaviso": round(monto_preaviso, 2),
                "dias_cesantias": dias_cesantias,
                "monto_cesantias": round(monto_cesantias, 2),
                "dias_vacaciones": dias_vacaciones,
                "monto_vacaciones": round(monto_vacaciones, 2),
                "monto_navidad": round(monto_navidad, 2),
                "total": round(total_liquidisacion, 2)
            }

    return render_template('tools/prestaciones.html', resultado=resultado, sueldo=sueldo, meses=meses_trabajados)