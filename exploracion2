from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/exploracion', methods=['GET', 'POST'])
def exploracion():
    if request.method == 'POST':
        # Получаем данные из формы
        observacion = request.form.get('observacion')
        palpacion = request.form.get('palpacion')
        movilizacion = request.form.get('movilizacion')
        tono_muscular = request.form.get('tono_muscular')
        pruebas = request.form.get('pruebas')

        # Обрабатываем данные
        resultados = {
            "observacion": observacion,
            "palpacion": palpacion,
            "movilizacion": movilizacion,
            "tono_muscular": tono_muscular,
            "pruebas": pruebas
        }
        diagnostico, recomendaciones = generar_diagnostico_y_recomendaciones(resultados)

        # Возвращаем результаты на страницу
        return render_template('resultados.html', resultados=resultados, diagnostico=diagnostico, recomendaciones=recomendaciones)

    return render_template('formulario.html')


def generar_diagnostico_y_recomendaciones(resultados):
    """Генерация диагноза и рекомендаций."""
    diagnostico = []
    if "inclinada" in resultados["observacion"].lower():
        diagnostico.append("Alteración en la postura con posible desequilibrio pélvico.")
    if "severo" in resultados["palpacion"].lower():
        diagnostico.append("Dolor severo en articulaciones con posible inflamación.")
    if "restricción severa" in resultados["movilizacion"].lower():
        diagnostico.append("Limitación severa del rango de movimiento.")
    if "hipotonía" in resultados["tono_muscular"].lower():
        diagnostico.append("Reducción del tono muscular en las extremidades posteriores.")
    if "ortolani positiva" in resultados["pruebas"].lower():
        diagnostico.append("Displasia de cadera severa confirmada.")

    diagnostico_final = " ".join(diagnostico) if diagnostico else "Sin hallazgos significativos."

    recomendaciones = []
    if "dolor severo" in resultados["palpacion"].lower() or "restricción severa" in resultados["movilizacion"].lower():
        recomendaciones.append("Terapia láser: 3-4 veces por semana para aliviar el dolor.")
    if "hipotonía" in resultados["tono_muscular"].lower():
        recomendaciones.append("Ejercicios de fortalecimiento: 2-3 veces por semana.")
    if "ortolani positiva" in resultados["pruebas"].lower():
        recomendaciones.append("Consulta con el veterinario para evaluar cirugía correctiva.")
    if not recomendaciones:
        recomendaciones.append("Monitoreo continuo sin intervención específica.")

    return diagnostico_final, recomendaciones


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
