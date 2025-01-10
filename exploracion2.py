from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/exploracion_funcional')
def exploracion_funcional():
    return render_template('exploracion_funcional.html')

@app.route('/exploracion_fisica', methods=['GET', 'POST'])
def exploracion_fisica():
    if request.method == 'POST':
        observacion = request.form.get('observacion')
        palpacion = request.form.get('palpacion')
        movilizacion = request.form.get('movilizacion')
        tono_muscular = request.form.get('tono_muscular')
        pruebas = request.form.get('pruebas')

        resultados_fisica = {
            "observacion": observacion,
            "palpacion": palpacion,
            "movilizacion": movilizacion,
            "tono_muscular": tono_muscular,
            "pruebas": pruebas
        }
        return redirect(url_for('exploracion_dinamica', **resultados_fisica))
    return render_template('formulario_fisica.html')

@app.route('/exploracion_dinamica', methods=['GET', 'POST'])
def exploracion_dinamica():
    if request.method == 'POST':
        paso_trote = request.form.get('paso_trote')
        circulos = request.form.get('circulos')
        escaleras = request.form.get('escaleras')
        postura = request.form.get('postura')
        tumbado = request.form.get('tumbado')

        resultados_dinamica = {
            "paso_trote": paso_trote,
            "circulos": circulos,
            "escaleras": escaleras,
            "postura": postura,
            "tumbado": tumbado
        }

        diagnostico, recomendaciones = generar_diagnostico_dinamico(resultados_dinamica)

        return render_template(
            'resultados.html',
            resultados_fisica=request.args,
            resultados_dinamica=resultados_dinamica,
            diagnostico=diagnostico,
            recomendaciones=recomendaciones
        )
    return render_template('formulario_dinamica.html')

def generar_diagnostico_dinamico(resultados):
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)