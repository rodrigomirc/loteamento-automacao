import os

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
        pausa(self.metrica.get("pausa_apos_ok3", 3.0))
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
        pausa(self.metrica["pausa_padrao"])
