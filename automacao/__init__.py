import time
import yaml


def carregar_config(caminho="config.yaml"):
    with open(caminho, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def pausa(segundos):
    time.sleep(segundos)


def normalizar_texto(texto):
    return str(texto).strip()
