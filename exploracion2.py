from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ваш_секретный_ключ'  # Установите секретный ключ для сессий

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
        # Сохраняем результаты в сессии
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
        # Извлекаем результаты физического осмотра из сессии
        resultados_fisica = session.get('resultados_fisica', {})
        # Объединяем результаты
        resultados_completос = {**resultados_fisica, **resultados_dinamica}
        diagnostico, recomendaciones = generar_diagnostico_completo(resultados_completос)
        return render_template('resultados.html', resultados=resultados_completос, diagnostico=diagnostico, recomendaciones=recomendaciones)
    return render_template('formulario_dinamica.html')

# Функции для генерации диагнозов
def generar_diagnostico_completo(resultados):
    """Генерация диагноза и рекомендаций на основе объединенных результатов."""
    diagnostico = []
    # Анализ результатов физического осмотра
    if "inclinada" in resultados.get("observacion", "").lower():
        diagnostico.append("Alteración en la postura con posible desequilibrio pélvico.")
    if "severo" in resultados.get("palpacion", "").lower():
        diagnostico.append("Dolor severo en articulaciones con posible inflamación.")
    # Анализ результатов динамического осмотра
    if "anormalidad" in resultados.get("paso_trote", "").lower():
        diagnostico.append("Anormalidad en el paso/trote detectada, posible cojera.")
    if "elevación" in resultados.get("circulos", "").lower():
        diagnostico.append("Elevación de cadera al caminar en círculos, posible displasia de cadera.")
    # Добавьте остальную логику...
    diagnostico_final = " ".join(diagnostico) if diagnostico else "Sin hallazgos significativos."
    recomendaciones = []
    if "dolor severo" in resultados.get("palpacion", "").lower():
        recomendaciones.append("Terapia láser para reducir el dolor.")
    # Добавьте рекомендации...
    return diagnostico_final, recomendaciones

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)