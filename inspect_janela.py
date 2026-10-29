from pywinauto import Application

app = Application(backend="uia").connect(title_re=".*Métrica DIMENSOR.*")
janela = app.window(title_re=".*Métrica DIMENSOR.*")

# Força a janela a ficar ativa
janela.set_focus()

# Desce por todos os níveis de controles e imprime botões, edits, tabs, etc.
def print_controls(control, nivel=0):
    try:
        nome = control.window_text()
        tipo = control.control_type()
        auto_id = control.automation_id()
        rect = control.rectangle()
        print("  " * nivel + f"{tipo} - '{nome}' | auto_id={auto_id} | rect={rect}")
    except Exception as e:
        print("  " * nivel + f"[Erro ao ler controle: {e}]")

    try:
        filhos = control.children()
        for filho in filhos:
            print_controls(filho, nivel + 1)
    except Exception as e:
        print("  " * (nivel + 1) + f"[Erro ao listar filhos: {e}]")

print_controls(janela)
