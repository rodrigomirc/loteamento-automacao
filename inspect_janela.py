import os
from datetime import datetime
from pywinauto import Application
from pywinauto.timings import TimeoutError
import pyautogui

# Cria pasta de logs se não existir
os.makedirs("logs", exist_ok=True)

# Conecta ao Métrica DIMENSOR
app = Application(backend="uia").connect(title_re=".*Métrica DIMENSOR.*")
janela = app.window(title_re=".*Métrica DIMENSOR.*")

# Traz a janela para frente
janela.set_focus()

# Tira screenshot da janela
caminho_screenshot = f"logs/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
try:
    img = janela.capture_as_image()
    img.save(caminho_screenshot)
    print(f"Screenshot salvo em: {caminho_screenshot}")
except Exception as e:
    print(f"Erro ao capturar janela: {e}")
    # Fallback: screenshot da tela toda
    pyautogui.screenshot(caminho_screenshot)
    print(f"Screenshot da tela toda salvo em: {caminho_screenshot}")

# Salva identificadores em arquivo de texto
caminho_ids = f"logs/identificadores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
try:
    with open(caminho_ids, "w", encoding="utf-8") as f:
        # Redireciona stdout temporariamente para o arquivo
        import sys
        stdout_original = sys.stdout
        sys.stdout = f
        janela.print_control_identifiers()
        sys.stdout = stdout_original
    print(f"Identificadores salvos em: {caminho_ids}")
except Exception as e:
    print(f"Erro ao salvar identificadores: {e}")

print("Mapeamento concluído.")
