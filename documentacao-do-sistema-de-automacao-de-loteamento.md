# Automação de Loteamento — Documentação

## Objetivo

Automatizar a análise e geração de arquivos de loteamento no software **Métrica DIMENSOR**, partindo de uma planilha de dados e salvando os arquivos nas pastas corretas.

## Fluxo automatizado

O sistema executa a sequência manual de **41 passos** para cada linha da planilha:

1. Clicar em **Novo** no Métrica DIMENSOR
2. Preencher nome do imóvel (TAB + digitar)
3. Clicar em **Avançar**
4. Selecionar **Importando informações de documentos**
5. Clicar em **Avançar** duas vezes
6. Duplo-clique no arquivo `MEMO_EM_BRANCO.DOC`
7. Clicar em **Não**
8. Colar a descrição do imóvel
9. Clicar em **Processar**
10. Confirmar diálogos com **OK**
11. Exportar para o **Google Earth Pro**
12. Salvar o KML na pasta do imóvel
13. Capturar print da área plotada
14. Salvar o print na pasta de Cálculos de Fechamento
15. Salvar o projeto final na pasta do imóvel

## Estrutura de pastas

```
C:\loteamento\
│
├── venv\                        # ambiente virtual Python
├── dados\
│   └── loteamentos.xlsx         # planilha com os dados de entrada
├── templates\
│   └── MEMO_EM_BRANCO.DOC       # arquivo template
├── logs\                        # screenshots e identificadores
├── config.yaml                  # configurações do sistema
├── main.py                      # execução principal
├── gerar_planilha.py            # cria a planilha modelo
├── posicao_mouse.py             # auxiliar para mapear coordenadas
├── automacao\
│   ├── __init__.py
│   ├── dimensor.py              # automação do Métrica DIMENSOR
│   ├── google_earth.py          # automação do Google Earth Pro
│   ├── print_screen.py          # captura de tela
│   └── utils.py                 # funções auxiliares
```

## Colunas da planilha

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `Nome` | Nome do loteamento/imovel | `Loteamento Alpha` |
| `Descricao` | Descrição completa do imóvel | `Loteamento...` |
| `Endereco` | Caminho da pasta do imóvel | `C:\Loteamentos\Alpha` |

## Resolução e ambiente

- Resolução da tela: **1440 x 900**
- Métrica DIMENSOR sempre **maximizado**
- Google Earth Pro **abre sozinho** durante o processo

## Configuração

Todas as coordenadas, caminhos e tempos de espera ficam no arquivo `config.yaml`. Assim você pode ajustar sem mexer no código.

## Avisos importantes

- A automação usa coordenadas fixas de tela. Funciona apenas se a janela do Métrica DIMENSOR estiver sempre no mesmo estado (maximizada, mesma resolução).
- Não mova o mouse nem use o computador durante a execução.
- O sistema não trata erros inesperados do Métrica DIMENSOR. Recomenda-se testar com poucas linhas primeiro.
- Nunca compartilhe a licença. O sistema trata o título da janela com regex, sem armazenar dados sensíveis.

## Como usar

1. **Instale as dependências** (preferencialmente em ambiente virtual com Python 3.12):

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. **Crie a planilha modelo**:

```bash
python gerar_planilha.py
```

3. **Copie o arquivo template**:

```bash
Copie MEMO_EM_BRANCO.DOC para templates\MEMO_EM_BRANCO.DOC
```

4. **Ajuste as coordenadas no `config.yaml`**:
   - Três coordenadas estão marcadas para revisão: `novo`, `avancar_2` e `salvar_print`
   - Use `python posicao_mouse.py` para verificar

5. **Preencha a planilha** `dados/loteamentos.xlsx`

6. **Execute**:

```bash
python main.py
```

## Ajuste de coordenadas

Use o script auxiliar:

```bash
python posicao_mouse.py
```

Posicione o mouse sobre cada botão e anote as coordenadas para atualizar o `config.yaml`.

## Manutenção

Se o layout do Métrica DIMENSOR mudar, atualize apenas as coordenadas no `config.yaml`.