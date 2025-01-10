from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Маршрут для начального выбора "Exploración Funcional"
@app.route('/exploracion_funcional')
def exploracion_funcional():
    return render_template('exploracion_funcional.html')

# Маршрут для "Exploración Física"
@app.route('/exploracion_fisica', methods=['GET', 'POST'])
def exploracion_fisica():
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
        request.form = resultados  # сохраняем результаты для следующего шага
        return redirect(url_for('exploracion_dinamica'))

    return render_template('formulario_fisica.html')

# Маршрут для "Exploración Dinámica"
@app.route('/exploracion_dinamica', methods=['GET', 'POST'])
def exploracion_dinamica():
    if request.method == 'POST':
        # Получаем данные из формы
        paso_trote = request.form.get('paso_trote')
        circulos = request.form.get('circulos')
        escaleras = request.form.get('escaleras')
        postura = request.form.get('postura')
        tumbado = request.form.get('tumbado')

        # Обрабатываем данные
        resultados = {
            "paso_trote": paso_trote,
            "circulos": circulos,
            "escaleras": escaleras,
            "postura": postura,
            "tumbado": tumbado
        }
        diagnostico, recomendaciones = generar_diagnostico_dinamico(resultados)

        # Возвращаем результаты на страницу
        return render_template('resultados_dinamica.html', resultados=resultados, diagnostico=diagnostico, recomendaciones=recomendaciones)

    return render_template('formulario_dinamica.html')

# Функции для генерации диагнозов
def generar_diagnostico_dinamico(resultados):
    """Генерация диагноза и рекомендаций для динамической оценки."""
    diagnostico = []
    if "anormalidad" in resultados["paso_trote"].lower():
        diagnostico.append("Anormalidad en el paso/trote detectada, posible cojera.")
    if "elevación" in resultados["circulos"].lower():
        diagnostico.append("Elevación de cadera al caminar en círculos, posible displasia de cadera.")
    if "dificultad" in resultados["escaleras"].lower():
        diagnostico.append("Dificultad para subir/bajar escaleras, posible dolor o restricción de movimiento.")
    if "postura inclinada" in resultados["postura"].lower():
        diagnostico.append("Postura inclinada, indicativo de desequilibrio pélvico.")
    if "dificultad" in resultados["tumbado"].lower():
        diagnostico.append("Dificultad para tumbarse o levantarse, posible dolor severo.")

    diagnostico_final = " ".join(diagnostico) if diagnostico else "Sin hallazgos significativos."

    recomendaciones = []
    if "anormalidad" in resultados["paso_trote"].lower() or "dificultad" in resultados["escaleras"].lower():
        recomendaciones.append("Terapia láser para reducir el dolor y mejorar la movilidad.")
    if "elevación" in resultados["circulos"].lower():
        recomendaciones.append("Ejercicios de fortalecimiento para las extremidades posteriores.")
    if not recomendaciones:
        recomendaciones.append("Monitoreo continuo sin intervención específica.")

    return diagnostico_final, recomendaciones

# Генерация диагноза для "Exploración Física" остается без изменений

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
