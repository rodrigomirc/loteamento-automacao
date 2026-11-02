import os
import time

import pandas as pd
import pyautogui

from automacao.reurb import ReurbAutomator
from automacao.utils import carregar_config, normalizar_texto


def processar_linha(dados, reurb):
    nome = normalizar_texto(dados["Nome"])
    endereco = normalizar_texto(dados["Endereco"])
    id_imovel = normalizar_texto(dados["ID"])

    print(f"\nSIG: {nome} (ID {id_imovel})")

    reurb.abrir_dms(nome, endereco)
    reurb.selecionar_camada_reurb()
    reurb.cadastrar_imovel(id_imovel)

    pyautogui.screenshot(os.path.join(endereco, f"{nome}_reurb.png"))
    print(f"  Finalizado: {nome}")


def main():
    config = carregar_config()
    df = pd.read_excel(config["caminhos"]["planilha"], engine="openpyxl")
    reurb = ReurbAutomator()
    espera = config["metrica_dimensor"]["pausa_entre_arquivos"]

    for _, linha in df.iterrows():
        try:
            processar_linha(linha, reurb)
        except Exception as e:
            print(f"  Erro em {linha.get('Nome', 'desconhecido')}: {e}")
        finally:
            try:
                reurb.fechar_programa()
            except Exception:
                pass
        print(f"Aguardando {espera}s antes do próximo...")
        time.sleep(espera)


if __name__ == "__main__":
    main()
