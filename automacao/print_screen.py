import os

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
