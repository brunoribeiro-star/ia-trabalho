from flask import Flask, render_template, request, jsonify
from colorize import gerar_paleta_cores
from adoptmizer import analisar_anuncios

app = Flask(__name__)

# Rota para exibir a interface
@app.route("/")
def index():
    return render_template("index.html")

# Rota para a colorize
@app.route("/gerar_paleta", methods=["POST"])
def gerar_paleta():
    descricao = request.json.get('descricao')
    resultado = gerar_paleta_cores(descricao)
    if "error" in resultado:
        return jsonify(error=resultado["error"])
    return jsonify(paleta=resultado["paleta"])

# Rota para o adoptimizer
@app.route("/analisar_anuncios", methods=["POST"])
def analisar():
    # Obtenção dos dados recebidos da requisição
    num_campanhas = request.json.get("numCampanhas")
    campanhas = request.json.get("campanhas")
    meta_cliques = request.json.get("metaCliques")
    meta_conversoes = request.json.get("metaConversoes")
    
    # Chama a função `analisar_anuncios` e captura o resultado
    resultado = analisar_anuncios(num_campanhas, campanhas, meta_cliques, meta_conversoes)
    
    # Verifica se há um erro e retorna o erro se houver
    if "error" in resultado:
        return jsonify({"error": resultado["error"]})
    
    # Retorna o resultado da análise como JSON
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
