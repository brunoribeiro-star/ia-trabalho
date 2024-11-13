import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import warnings

# Ignorar avisos de divisão por zero
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Função para IA de análise de anúncios (interativa)
def analisar_anuncios_interativo():
    data, meta_cliques, meta_conversoes = solicitar_dados()
    if len(data) < 2:
        print("\nAviso: Para realizar uma análise de regressão confiável, insira pelo menos duas campanhas.")
    else:
        plt.figure(figsize=(8, 5))
        plt.scatter(data['gastos'], data['cliques'], color='blue')
        plt.xlabel('Gastos')
        plt.ylabel('Cliques')
        plt.title('Gastos vs Cliques')
        plt.show()

        plt.figure(figsize=(8, 5))
        plt.scatter(data['gastos'], data['conversões'], color='green')
        plt.xlabel('Gastos')
        plt.ylabel('Conversões')
        plt.title('Gastos vs Conversões')
        plt.show()

        plt.figure(figsize=(8, 5))
        plt.scatter(data['cpa'], data['conversões'], color='purple')
        plt.xlabel('CPA')
        plt.ylabel('Conversões')
        plt.title('CPA vs Conversões')
        plt.show()

        x = data[['gastos']]
        y_cliques = data['cliques']
        y_conversoes = data['conversões']

        modelo_cliques = LinearRegression()
        modelo_cliques.fit(x, y_cliques)
        modelo_conversoes = LinearRegression()
        modelo_conversoes.fit(x, y_conversoes)

        gastos_para_cliques = (meta_cliques - modelo_cliques.intercept_) / modelo_cliques.coef_[0]
        gastos_para_conversoes = (meta_conversoes - modelo_conversoes.intercept_) / modelo_conversoes.coef_[0]

        print(f"\nPara atingir {meta_cliques} cliques, os gastos recomendados são aproximadamente: R$ {gastos_para_cliques:.2f}")
        print(f"Para atingir {meta_conversoes} conversões, os gastos recomendados são aproximadamente: R$ {gastos_para_conversoes:.2f}")

def solicitar_dados():
    num_campanhas = int(input("Quantas campanhas deseja analisar? "))
    campanhas = []
    for i in range(num_campanhas):
        print(f"\nInforme os dados atuais da sua campanha {i + 1}:")
        campanhas.append({
            'gastos': float(input("Gastos (em R$): ")),
            'cliques': int(input("Cliques: ")),
            'impressões': int(input("Impressões: ")),
            'conversões': int(input("Conversões: ")),
            'cpa': float(input("CPA (Custo por Aquisição): ")),
            'publico_alvo': input("Público-alvo: "),
            'horario': input("Horário: "),
            'dia_da_semana': input("Dia da semana: "),
            'plataforma': input("Plataforma: "),
            'dispositivo': input("Dispositivo: ")
        })
    meta_cliques = int(input("\nInforme a meta desejada de cliques: "))
    meta_conversoes = int(input("Informe a meta desejada de conversões: "))
    return pd.DataFrame(campanhas), meta_cliques, meta_conversoes

# Função para análise de anúncios para integração com front-end
def analisar_anuncios(num_campanhas, campanhas, meta_cliques, meta_conversoes):
    # Converte a lista de campanhas para um DataFrame
    data = pd.DataFrame(campanhas)
    
    if len(data) < 2:
        return {"error": "Para realizar uma análise de regressão confiável, insira pelo menos duas campanhas."}

    # Gráficos para visualização (pode ser removido ou adaptado para retorno em JSON se necessário)
    plt.figure(figsize=(8, 5))
    plt.scatter(data['gastos'], data['cliques'], color='blue')
    plt.xlabel('Gastos')
    plt.ylabel('Cliques')
    plt.title('Gastos vs Cliques')
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.scatter(data['gastos'], data['conversões'], color='green')
    plt.xlabel('Gastos')
    plt.ylabel('Conversões')
    plt.title('Gastos vs Conversões')
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.scatter(data['cpa'], data['conversões'], color='purple')
    plt.xlabel('CPA')
    plt.ylabel('Conversões')
    plt.title('CPA vs Conversões')
    plt.show()

    # Regressão linear para prever cliques e conversões
    x = data[['gastos']]
    y_cliques = data['cliques']
    y_conversoes = data['conversões']

    modelo_cliques = LinearRegression()
    modelo_cliques.fit(x, y_cliques)
    modelo_conversoes = LinearRegression()
    modelo_conversoes.fit(x, y_conversoes)

    # Calcula os gastos necessários para atingir as metas
    gastos_para_cliques = (meta_cliques - modelo_cliques.intercept_) / modelo_cliques.coef_[0]
    gastos_para_conversoes = (meta_conversoes - modelo_conversoes.intercept_) / modelo_conversoes.coef_[0]

    # Retorna os resultados em um formato de dicionário
    return {
        "gastos_para_meta_cliques": round(gastos_para_cliques, 2),
        "gastos_para_meta_conversoes": round(gastos_para_conversoes, 2)
    }
