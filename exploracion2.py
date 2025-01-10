from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Ключ для работы с сессиями

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
        resultados_fisica = {
            "observacion": request.form.get('observacion'),
            "palpacion": request.form.get('palpacion'),
            "movilizacion": request.form.get('movilizacion'),
            "tono_muscular": request.form.get('tono_muscular'),
            "pruebas": request.form.get('pruebas')
        }
        # Сохраняем результаты в сессию
        session['resultados_fisica'] = resultados_fisica
        return redirect(url_for('exploracion_dinamica'))

    return render_template('formulario_fisica.html')

# Маршрут для "Exploración Dinámica"
@app.route('/exploracion_dinamica', methods=['GET', 'POST'])
def exploracion_dinamica():
    if request.method == 'POST':
        # Получаем данные из формы
        resultados_dinamica = {
            "paso_trote": request.form.get('paso_trote'),
            "circulos": request.form.get('circulos'),
            "escaleras": request.form.get('escaleras'),
            "postura": request.form.get('postura'),
            "tumbado": request.form.get('tumbado')
        }
        # Сохраняем результаты динамической проверки в сессию
        session['resultados_dinamica'] = resultados_dinamica

        # Генерируем диагнозы
        diagnostico, recomendaciones = generar_diagnostico_completo()

        # Возвращаем результаты на страницу
        return render_template('resultados.html', diagnostico=diagnostico, recomendaciones=recomendaciones)

    return render_template('formulario_dinamica.html')

# Генерация диагнозов и рекомендаций
def generar_diagnostico_completo():
    # Получаем данные из сессии
    resultados_fisica = session.get('resultados_fisica', {})
    resultados_dinamica = session.get('resultados_dinamica', {})

    # Генерация диагноза и рекомендаций для физической оценки
    diagnostico = []
    if "inclinada" in resultados_fisica.get("observacion", "").lower():
        diagnostico.append("Alteración en la postura con posible desequilibrio pélvico.")
    if "severo" in resultados_fisica.get("palpacion", "").lower():
        diagnostico.append("Dolor severo en articulaciones con posible inflamación.")
    if "restricción severa" in resultados_fisica.get("movilizacion", "").lower():
        diagnostico.append("Limitación severa del rango de movimiento.")
    if "hipotonía" in resultados_fisica.get("tono_muscular", "").lower():
        diagnostico.append("Reducción del tono muscular en las extremidades posteriores.")
    if "ortolani positiva" in resultados_fisica.get("pruebas", "").lower():
        diagnostico.append("Displasia de cadera severa confirmada.")

    # Генерация диагноза и рекомендаций для динамической оценки
    if "anormalidad" in resultados_dinamica.get("paso_trote", "").lower():
        diagnostico.append("Anormalidad en el paso/trote detectada, posible cojera.")
    if "elevación" in resultados_dinamica.get("circulos", "").lower():
        diagnostico.append("Elevación de cadera al caminar en círculos, posible displasia de cadera.")
    if "dificultad" in resultados_dinamica.get("escaleras", "").lower():
        diagnostico.append("Dificultad para subir/bajar escaleras, posible dolor o restricción de movimiento.")
    if "postura inclinada" in resultados_dinamica.get("postura", "").lower():
        diagnostico.append("Postura inclinada, indicativo de desequilibrio pélvico.")
    if "dificultad" in resultados_dinamica.get("tumbado", "").lower():
        diagnostico.append("Dificultad para tumbarse o levantarse, posible dolor severo.")

    diagnostico_final = " ".join(diagnostico) if diagnostico else "Sin hallazgos significativos."

    recomendaciones = []
    if "dolor severo" in resultados_fisica.get("palpacion", "").lower() or "restricción severa" in resultados_fisica.get("movilizacion", "").lower():
        recomendaciones.append("Terapia láser: 3-4 veces por semana para aliviar el dolor.")
    if "hipotonía" in resultados_fisica.get("tono_muscular", "").lower():
        recomendaciones.append("Ejercicios de fortalecimiento: 2-3 veces por semana.")
    if "ortolani positiva" in resultados_fisica.get("pruebas", "").lower():
        recomendaciones.append("Consulta con el veterinario para evaluar cirugía correctiva.")
    if "anormalidad" in resultados_dinamica.get("paso_trote", "").lower() or "dificultad" in resultados_dinamica.get("escaleras", "").lower():
        recomendaciones.append("Terapia láser para reducir el dolor y mejorar la movilidad.")
    if "elevación" in resultados_dinamica.get("circulos", "").lower():
        recomendaciones.append("Ejercicios de fortalecimiento para las extremidades posteriores.")
    if not recomendaciones:
        recomendaciones.append("Monitoreo continuo sin intervención específica.")

    return diagnostico_final, recomendaciones

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
