import os

import pandas as pd

from automacao.dimensor import DimensorAutomator
from automacao.google_earth import GoogleEarthAutomator
from automacao.print_screen import PrintScreenAutomator
from automacao.utils import carregar_config, normalizar_texto


def garantir_pastas(endereco):
    os.makedirs(endereco, exist_ok=True)


def processar_linha(dados, dimensor, google_earth, print_screen):
    nome = normalizar_texto(dados["Nome"])
    descricao = normalizar_texto(dados["Descricao"])
    endereco = normalizar_texto(dados["Endereco"])

    print(f"\nProcessando: {nome}")
    print(f"  -> {endereco}")

    garantir_pastas(endereco)

    # Métrica DIMENSOR
    dimensor.conectar()
    dimensor.novo_projeto(nome)
    dimensor.importar_memo()
    dimensor.inserir_descricao(descricao)
    dimensor.processar()
    dimensor.exportar_google_earth()

    # Google Earth Pro
    google_earth.salvar_kml(nome, endereco)
    google_earth.minimizar()

    # Captura de tela
    print_screen.capturar_area_plotada()
    print_screen.salvar_print(nome)

    # Salvar projeto final
    dimensor.conectar()
    dimensor.clicar("salvar_projeto")
    dimensor.digitar(nome)
    dimensor.clicar("campo_endereco_projeto")
    dimensor.digitar(endereco)
    dimensor.pressionar("enter")
    dimensor.clicar("salvar_projeto_final")

    print(f"  ✅ Finalizado: {nome}")


def main():
    config = carregar_config()
    df = pd.read_excel(config["caminhos"]["planilha"], engine="openpyxl")

    dimensor = DimensorAutomator()
    google_earth = GoogleEarthAutomator()
    print_screen = PrintScreenAutomator()

    for _, linha in df.iterrows():
        try:
            processar_linha(linha, dimensor, google_earth, print_screen)
        except Exception as e:
            print(f"  ❌ Erro ao processar {linha.get('Nome', 'desconhecido')}: {e}")


if __name__ == "__main__":
    main()
