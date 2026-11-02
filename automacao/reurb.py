import os

import pyautogui
from pywinauto import Application

from .dimensor import DimensorAutomator
from .utils import pausa


class ReurbAutomator(DimensorAutomator):

    def colar_em(self, coordenada, texto):
        self.clicar(coordenada)
        pyautogui.hotkey("ctrl", "a")
        self.digitar(str(texto))

    def abrir_dms(self, nome, endereco):
        caminho_dms = os.path.join(endereco, f"{nome}.dms")
        if not os.path.exists(caminho_dms):
            raise FileNotFoundError(caminho_dms)

        os.startfile(caminho_dms)
        pausa(self.metrica["pausa_abrir_dms"])

        self.app = Application(backend="uia").connect(
            title_re=self.metrica["titulo_regex"], timeout=30
        )
        self.janela = self.app.window(title_re=self.metrica["titulo_regex"])
        self.janela.wait("ready", timeout=30)
        self.janela.set_focus()
        if self.metrica["maximizado"]:
            self.janela.maximize()
        pausa(self.metrica["pausa_dialogo"])

    def fechar_programa(self):
        try:
            self.janela.close()
            pausa(self.metrica["pausa_fechar"])
        except Exception:
            pass
        # Se o programa ainda estiver aberto, força o encerramento
        if self.app.is_process_running():
            self.app.kill()
            pausa(self.metrica["pausa_fechar"])

    def selecionar_camada_reurb(self):
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("botao_sig")
        pausa(self.metrica["pausa_sig"])
        self.clicar("escolher_camada")
        pausa(self.metrica["pausa_padrao"])
        self.clicar("opcao_reurb")
        pausa(self.metrica["pausa_padrao"])
        self.clicar("ok_camada")
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("sim_camada_1")
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("sim_camada_2")
        pausa(self.metrica["pausa_apos_ok3"])

    def cadastrar_imovel(self, id_imovel):
        self.clicar("cadastrar")
        pausa(self.metrica["pausa_padrao"])
        self.colar_em("campo_matricula", id_imovel)
        pausa(self.metrica["pausa_padrao"])
        self.colar_em("campo_nome_imovel", id_imovel)
        pausa(self.metrica["pausa_padrao"])
        self.clicar("salvar_cadastro")
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("ok_cadastro")
        pausa(self.metrica["pausa_apos_ok2"])
        self.clicar("vincular")
        pausa(self.metrica["pausa_dialogo"])
        self.clicar("fechar_sig")
        pausa(self.metrica["pausa_dialogo"])
