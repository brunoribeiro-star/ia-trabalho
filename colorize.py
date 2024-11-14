import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
import random
import matplotlib.colors as mcolors
import colorsys
import warnings
import re

warnings.filterwarnings("ignore", category=RuntimeWarning)

def gerar_paleta_cores(descricao):
    tipo_paleta, cores_base = interpretar_descricao(descricao)

    if tipo_paleta == "complementar":
        paleta = gerar_paleta_complementar_aleatoria(cores_base)
    elif tipo_paleta == "monocromatica":
        paleta = gerar_paleta_monocromatica_aleatoria(cores_base)
    elif tipo_paleta == "duas_cores":
        paleta = gerar_paleta_duas_cores(cores_base)
    else:
        return {"error": "Não entendi a solicitação. Por favor, forneça mais detalhes."}
    
    return {"paleta": paleta}

def interpretar_descricao(descricao):
    cores_hex = re.findall(r'#([A-Fa-f0-9]{6})', descricao)
    cores_base = ['#' + cor for cor in cores_hex] if cores_hex else []

    cor_keywords = {
        "vermelho": "#FF0000",
        "azul": "#0000FF",
        "verde": "#00FF00",
        "amarelo": "#FFFF00",
        "roxo": "#A703AF",
        "laranja": "#FFA500",
        "preto": "#000000",
        "branco": "#FFFFFF",
        "cinza": "#808080",
        "marrom": "#8B4513"
    }
    for nome_cor, hex_cor in cor_keywords.items():
        if nome_cor in descricao and hex_cor not in cores_base:
            cores_base.append(hex_cor)

    if "combinem com" in descricao or "combinar com" in descricao:
        tipo_paleta = "complementar"
    elif "tons de" in descricao or "monocromática" in descricao:
        tipo_paleta = "monocromatica"
    elif len(cores_base) == 2:
        tipo_paleta = "duas_cores"
    else:
        tipo_paleta = None

    return tipo_paleta, cores_base

def hex_to_rgb(hex_color):
    return mcolors.hex2color(hex_color)

def rgb_to_hex(rgb_color):
    return mcolors.to_hex(rgb_color)

def gerar_paleta_complementar_aleatoria(cores_base):
    paleta = []
    for cor_base in cores_base:
        base_rgb = hex_to_rgb(cor_base)
        base_hls = colorsys.rgb_to_hls(*base_rgb)
        paleta.append(cor_base)
        for i in range(5):
            hue_variation = (base_hls[0] + random.uniform(-0.2, 0.2)) % 1.0
            lightness_variation = min(1, max(0, base_hls[1] + random.uniform(-0.3, 0.3)))
            varied_hls = (hue_variation, lightness_variation, random.uniform(0.5, 1))
            varied_rgb = colorsys.hls_to_rgb(*varied_hls)
            paleta.append(rgb_to_hex(varied_rgb))
    return list(dict.fromkeys(paleta))[:6]

def gerar_paleta_monocromatica_aleatoria(cores_base):
    paleta = []
    for cor_base in cores_base:
        base_rgb = hex_to_rgb(cor_base)
        base_hls = colorsys.rgb_to_hls(*base_rgb)
        paleta.append(cor_base)
        for i in range(4):
            lightness_variation = base_hls[1] + (random.uniform(-0.3, 0.3) * i)
            varied_hls = (base_hls[0], min(1, max(0, lightness_variation)), base_hls[2])
            varied_rgb = colorsys.hls_to_rgb(*varied_hls)
            paleta.append(rgb_to_hex(varied_rgb))
    return list(dict.fromkeys(paleta))[:6]

def gerar_paleta_duas_cores(cores_base):
    paleta = []
    for cor_base in cores_base[:2]:
        base_rgb = hex_to_rgb(cor_base)
        base_hls = colorsys.rgb_to_hls(*base_rgb)
        paleta.append(cor_base)
        for i in range(2):
            lightness_variation = min(1, max(0, base_hls[1] + random.uniform(-0.3, 0.3)))
            varied_hls = (base_hls[0], lightness_variation, base_hls[2])
            varied_rgb = colorsys.hls_to_rgb(*varied_hls)
            paleta.append(rgb_to_hex(varied_rgb))
    return list(dict.fromkeys(paleta))[:6]