import os

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
