from flask import Flask, render_template, request, jsonify
from colorize import gerar_paleta_cores
from adoptmizer import analisar_anuncios

app = Flask(__name__)

#rota para exibir a interface
@app.route("/")
def index():
    return render_template("index.html")

#rota para a colorize
@app.route("/gerar_paleta", methods=["POST"])
def gerar_paleta():
    descricao = request.json.get('descricao')
    resultado = gerar_paleta_cores(descricao)
    if "error" in resultado:
        return jsonify(error=resultado["error"])
    return jsonify(paleta=resultado["paleta"])

#rota para o adoptimizer
@app.route("/analisar_anuncios", methods=["POST"])
def analisar():
    num_campanhas = request.json.get("numCampanhas")
    campanhas = request.json.get("campanhas")
    meta_cliques = request.json.get("metaCliques")
    meta_conversoes = request.json.get("metaConversoes")
    resultado = analisar_anuncios(num_campanhas, campanhas, meta_cliques, meta_conversoes) #chama a função no arquivo adoptimizer.py
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)