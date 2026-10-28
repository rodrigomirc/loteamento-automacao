import os
import subprocess
import sys

# Pasta base do projeto
PASTA_BASE = r"C:\loteamento"

# Conteúdo de cada arquivo do sistema
ARQUIVOS = {
    ".gitignore": r"""venv/
__pycache__/
*.pyc
*.xlsx
*.log

# Arquivos temporarios do Excel
~$*.xlsx
~$*.xls
""",

    "requirements.txt": r"""pandas
openpyxl
pywinauto
pyautogui
pyperclip
pyyaml
""",

    "config.yaml": r"""# Configuracao do sistema de automacao de loteamento
# Ajuste as coordenadas de acordo com sua tela (1440x900)

resolucao:
  largura: 1440
  altura: 900

caminhos:
  planilha: "dados/loteamentos.xlsx"
  template_memo: "templates/MEMO_EM_BRANCO.DOC"
  pasta_logs: "logs"

metrica_dimensor:
  titulo_regex: ".*Metrica DIMENSOR.*"
  maximizado: true
  # Tempo de espera entre acoes (segundos)
  pausa_padrao: 1.0
  pausa_dialogo: 2.0

coordenadas:
  # ATENCAO: tres coordenadas abaixo precisam de verificacao
  novo: [38, 104]              # ajustar se necessario
  avancar_1: [1011, 592]
  importar_documentos: [566, 515]
  avancar_2: [866, 614]        # ajustar se necessario
  avancar_3: [1141, 611]
  memo_em_branco: [586, 238]
  botao_nao: [867, 522]
  area_descricao: [697, 495]
  processar: [1177, 159]
  ok_1: [638, 742]
  ok_2: [653, 674]
  google: [152, 700]
  sim_1: [777, 520]
  ok_3: [678, 526]
  salvar_kml: [526, 175]
  salvar_kml_botao: [549, 249]
  campo_pasta_kml: [1120, 104]
  salvar_confirmacao: [1270, 701]
  sim_2: [791, 509]
  minimizar_google_earth: [1322, 914]
  fechar_area_plotada: [1206, 93]
  clicar_janela_print: [713, 387]
  notificacao_print: [1248, 605]
  campo_endereco_print: [855, 93]
  salvar_print: [998, 655]      # ajustar se necessario
  fechar_captura_print: [1371, 15]
  cancelar: [639, 607]
  salvar_projeto: [331, 93]
  campo_endereco_projeto: [1126, 109]
  salvar_projeto_final: [1269, 699]

atalhos:
  tab: "tab"
  f6: "f6"
  print_tela: "win+shift+s"
  salvar: "ctrl+s"
  enter: "enter"

pasta_calculos_fechamento: "\\\\192.168.1.1\\Rede Cartorio\\5 Registro\\Plotagem\\DIMENSOR - BEM TOPOGRAFIA\\REURB - CARMELITA ARRIEIRO\\Calculos de Fechamento"
""",

    "main.py": r"""import os

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

    # Metrica DIMENSOR
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

    print(f"  Finalizado: {nome}")


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
            print(f"  Erro ao processar {linha.get('Nome', 'desconhecido')}: {e}")


if __name__ == "__main__":
    main()
""",

    "gerar_planilha.py": r"""import os

import pandas as pd


def criar_planilha_modelo(caminho="dados/loteamentos.xlsx"):
    '''
    Cria uma planilha Excel modelo com as colunas necessarias.
    '''
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    dados = [
        {
            "Nome": "Exemplo Loteamento",
            "Descricao": "Descricao completa do imovel/loteamento.",
            "Endereco": "C:\\Loteamentos\\Exemplo",
        }
    ]

    df = pd.DataFrame(dados)
    df.to_excel(caminho, index=False, engine="openpyxl")
    print(f"Planilha modelo criada em: {os.path.abspath(caminho)}")


if __name__ == "__main__":
    criar_planilha_modelo()
""",

    "posicao_mouse.py": r"""import time

import pyautogui


def main():
    print("Mova o mouse para o local desejado.")
    print("Pressione Ctrl+C para parar.")
    print()

    try:
        while True:
            x, y = pyautogui.position()
            print(f"Posicao do mouse: x={x}, y={y}", end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nFinalizado.")


if __name__ == "__main__":
    main()
""",

    "automacao/__init__.py": r"""# Pacote de automacao do sistema de loteamento
""",

    "automacao/utils.py": r"""import time
import yaml


def carregar_config(caminho="config.yaml"):
    with open(caminho, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def pausa(segundos):
    time.sleep(segundos)


def normalizar_texto(texto):
    return str(texto).strip()
""",

    "automacao/dimensor.py": r"""import os

import pyautogui
import pyperclip
from pywinauto import Application

from .utils import carregar_config, normalizar_texto, pausa


class DimensorAutomator:
    def __init__(self):
        self.config = carregar_config()
        self.coords = self.config["coordenadas"]
        self.atalhos = self.config["atalhos"]
        self.metrica = self.config["metrica_dimensor"]
        self.janela = None

    def conectar(self):
        app = Application(backend="uia").connect(
            title_re=self.metrica["titulo_regex"]
        )
        self.janela = app.window(title_re=self.metrica["titulo_regex"])
        self.janela.set_focus()
        if self.metrica["maximizado"]:
            self.janela.maximize()
        pausa(self.metrica["pausa_padrao"])

    def clicar(self, nome_coordenada):
        x, y = self.coords[nome_coordenada]
        pyautogui.click(x, y)
        pausa(self.metrica["pausa_padrao"])

    def duplo_clique(self, nome_coordenada):
        x, y = self.coords[nome_coordenada]
        pyautogui.doubleClick(x, y)
        pausa(self.metrica["pausa_padrao"])

    def digitar(self, texto):
        pyperclip.copy(texto)
        pyautogui.hotkey("ctrl", "v")
        pausa(self.metrica["pausa_padrao"])

    def pressionar(self, tecla):
        pyautogui.press(tecla)
        pausa(self.metrica["pausa_padrao"])

    def hotkey(self, *teclas):
        pyautogui.hotkey(*teclas)
        pausa(self.metrica["pausa_padrao"])

    def novo_projeto(self, nome):
        self.clicar("novo")
        self.pressionar(self.atalhos["tab"])
        self.digitar(nome)
        self.clicar("avancar_1")

    def importar_memo(self):
        self.clicar("importar_documentos")
        self.clicar("avancar_2")
        self.clicar("avancar_3")
        self.duplo_clique("memo_em_branco")
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("botao_nao")

    def inserir_descricao(self, descricao):
        self.clicar("area_descricao")
        self.digitar(descricao)

    def processar(self):
        self.clicar("processar")
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("ok_1")
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("ok_2")

    def exportar_google_earth(self):
        self.clicar("google")
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("sim_1")
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("ok_3")
""",

    "automacao/google_earth.py": r"""import os

import pyautogui
import pyperclip

from .utils import carregar_config, pausa


class GoogleEarthAutomator:
    def __init__(self):
        self.config = carregar_config()
        self.coords = self.config["coordenadas"]
        self.atalhos = self.config["atalhos"]
        self.metrica = self.config["metrica_dimensor"]

    def clicar(self, nome_coordenada):
        x, y = self.coords[nome_coordenada]
        pyautogui.click(x, y)
        pausa(self.metrica["pausa_padrao"])

    def digitar(self, texto):
        pyperclip.copy(texto)
        pyautogui.hotkey("ctrl", "v")
        pausa(self.metrica["pausa_padrao"])

    def pressionar(self, tecla):
        pyautogui.press(tecla)
        pausa(self.metrica["pausa_padrao"])

    def salvar_kml(self, nome, endereco):
        self.clicar("salvar_kml")
        pausa(self.metrica["pausa_padrao"])
        self.clicar("salvar_kml_botao")
        pausa(self.metrica["pausa_padrao"])
        self.digitar(nome)
        self.clicar("campo_pasta_kml")
        self.digitar(endereco)
        self.pressionar(self.atalhos["enter"])
        pausa(self.metrica["pausa_padrao"])
        self.clicar("salvar_confirmacao")
        pausa(self.metrica["pausa_padrao"])
        self.clicar("sim_2")

    def minimizar(self):
        self.clicar("minimizar_google_earth")
""",

    "automacao/print_screen.py": r"""import os

import pyautogui
import pyperclip

from .utils import carregar_config, pausa


class PrintScreenAutomator:
    def __init__(self):
        self.config = carregar_config()
        self.coords = self.config["coordenadas"]
        self.atalhos = self.config["atalhos"]
        self.metrica = self.config["metrica_dimensor"]
        self.pasta_calculos = self.config["pasta_calculos_fechamento"]

    def clicar(self, nome_coordenada):
        x, y = self.coords[nome_coordenada]
        pyautogui.click(x, y)
        pausa(self.metrica["pausa_padrao"])

    def digitar(self, texto):
        pyperclip.copy(texto)
        pyautogui.hotkey("ctrl", "v")
        pausa(self.metrica["pausa_padrao"])

    def pressionar(self, tecla):
        pyautogui.press(tecla)
        pausa(self.metrica["pausa_padrao"])

    def hotkey(self, *teclas):
        pyautogui.hotkey(*teclas)
        pausa(self.metrica["pausa_padrao"])

    def capturar_area_plotada(self):
        self.clicar("fechar_area_plotada")
        self.pressionar(self.atalhos["f6"])
        self.hotkey(*self.atalhos["print_tela"].split("+"))
        pausa(1.5)
        self.clicar("clicar_janela_print")
        pausa(1.0)
        self.clicar("notificacao_print")
        pausa(1.0)
        self.hotkey(*self.atalhos["salvar"].split("+"))

    def salvar_print(self, nome):
        self.digitar(nome)
        self.clicar("campo_endereco_print")
        self.digitar(self.pasta_calculos)
        self.pressionar(self.atalhos["enter"])
        pausa(self.metrica["pausa_padrao"])
        self.clicar("salvar_print")
        pausa(self.metrica["pausa_padrao"])
        self.clicar("fechar_captura_print")
        pausa(self.metrica["pausa_padrao"])
        self.clicar("cancelar")
""",
}


def criar_pastas():
    """Cria a estrutura de pastas do projeto."""
    pastas = [
        "automacao",
        "dados",
        "templates",
        "logs",
    ]
    for pasta in pastas:
        caminho = os.path.join(PASTA_BASE, pasta)
        os.makedirs(caminho, exist_ok=True)
        print(f"Pasta criada/verificada: {caminho}")


def criar_arquivos():
    """Cria todos os arquivos do sistema, sobrescrevendo se necessario."""
    for caminho_relativo, conteudo in ARQUIVOS.items():
        caminho_completo = os.path.join(PASTA_BASE, caminho_relativo)
        os.makedirs(os.path.dirname(caminho_completo), exist_ok=True)
        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"Arquivo criado/atualizado: {caminho_completo}")


def criar_planilha_modelo():
    """Executa o script gerar_planilha.py para criar a planilha modelo."""
    script = os.path.join(PASTA_BASE, "gerar_planilha.py")
    print(f"\nCriando planilha modelo...")
    subprocess.run([sys.executable, script], cwd=PASTA_BASE, check=True)


def main():
    print(f"Criando estrutura do projeto em: {PASTA_BASE}")
    print("=" * 60)

    criar_pastas()
    criar_arquivos()
    criar_planilha_modelo()

    print("=" * 60)
    print("Estrutura criada com sucesso!")
    print("\nProximos passos:")
    print("1. Copie o arquivo MEMO_EM_BRANCO.DOC para a pasta templates/")
    print("2. Ajuste as coordenadas no config.yaml")
    print("3. Preencha a planilha dados/loteamentos.xlsx")
    print("4. Execute: python main.py")


if __name__ == "__main__":
    main()