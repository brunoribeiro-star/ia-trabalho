from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from colorize import gerar_paleta_cores
from adoptmizer import analisar_anuncios
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)

def plot_to_base64():
    plt.figure()
    plt.plot([1, 2, 3], [1, 2, 3])
    plt.title("Demo Plot")
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar_paleta", methods=["POST"])
def gerar_paleta():
    descricao = request.json.get('descricao')
    if not descricao:
        return jsonify(error="Descrição não fornecida"), 400
    resultado = gerar_paleta_cores(descricao)
    if "error" in resultado:
        return jsonify(error=resultado["error"]), 400
    return jsonify(paleta=resultado["paleta"])

@app.route("/analisar_anuncios", methods=["POST"])
def analisar():
    try:
        data = request.get_json()
        if not data or 'campanhas' not in data or 'meta_cliques' not in data or 'meta_conversoes' not in data:
            return jsonify({'error': 'Dados incompletos ou mal formatados'}), 400

        campanhas = data['campanhas']
        meta_cliques = data['meta_cliques']
        meta_conversoes = data['meta_conversoes']

        resultado = analisar_anuncios(campanhas, meta_cliques, meta_conversoes)
        grafico = plot_to_base64()
        resultado['grafico'] = grafico
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
