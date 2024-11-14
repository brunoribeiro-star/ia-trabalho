import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def analisar_anuncios(campanhas, meta_cliques, meta_conversoes):
    if not campanhas:
        return {"error": "Nenhuma campanha foi adicionada."}

    data = pd.DataFrame(campanhas)

    total_gastos = data['gastos'].sum()
    total_cliques = data['cliques'].sum()
    total_conversoes = data['conversoes'].sum()

    if total_cliques == 0 or total_conversoes == 0:
        return {"error": "Os dados atuais não têm cliques ou conversões para análise."}

    gastos_necessarios_cliques = (meta_cliques * total_gastos) / total_cliques if total_cliques > 0 else float('inf')
    gastos_necessarios_conversoes = (meta_conversoes * total_gastos) / total_conversoes if total_conversoes > 0 else float('inf')

    gastos_totais_necessarios = max(gastos_necessarios_cliques, gastos_necessarios_conversoes)

    return {
        "gastos_totais_necessarios": round(gastos_totais_necessarios, 2),
        "gastos_para_cliques": round(gastos_necessarios_cliques, 2),
        "gastos_para_conversoes": round(gastos_necessarios_conversoes, 2)
    }
