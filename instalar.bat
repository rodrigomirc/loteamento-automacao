@echo off
chcp 65001 >nul
title Instalacao - Sistema de Automacao de Loteamento
color 0A

echo ============================================
echo  Instalador do Sistema de Loteamento
echo  Pasta: C:\loteamento
echo ============================================
echo.

cd /d C:\loteamento

REM Verifica se o Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado.
    echo Baixe e instale o Python 3.11 ou superior em https://www.python.org
    echo Marque a opcao "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

echo [OK] Python encontrado:
python --version
echo.

REM Cria o ambiente virtual
if exist "venv" (
    echo [AVISO] Ambiente virtual ja existe. Pulando criacao.
) else (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar o ambiente virtual.
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado.
)
echo.

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Atualiza o pip
echo [INFO] Atualizando pip...
python -m pip install --upgrade pip

REM Instala as dependencias
echo [INFO] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  [OK] Instalacao concluida com sucesso!
echo ============================================
echo.
echo Proximos passos:
echo 1. Instale o Metrica DIMENSOR.
echo 2. Instale o Google Earth Pro.
echo 3. Instale o Microsoft Excel.
echo 4. Copie o arquivo MEMO_EM_BRANCO.DOC para:
echo    C:\loteamento\templates\
echo 5. Ajuste as coordenadas no config.yaml usando:
echo    python posicao_mouse.py
echo 6. Preencha a planilha em:
echo    C:\loteamento\dados\loteamentos.xlsx
echo 7. Execute o sistema com:
echo    venv\Scripts\activate ^&^& python main.py
echo.
pause
