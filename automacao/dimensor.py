import os

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
