#!/bin/bash

# Caminho absoluto para a pasta do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Arquivo de configuração dentro da pasta "scripts"
CONFIG_FILE="$SCRIPT_DIR/tree.conf"

# Diretório onde a estrutura deve ser criada (um nível acima)
TARGET_DIR="$(dirname "$SCRIPT_DIR")"

echo "Criando estrutura em: $TARGET_DIR"
echo "Usando o arquivo de configuração: $CONFIG_FILE"
echo ""

###############################################################################
# 1. Criar estrutura de pastas e arquivos
###############################################################################

while IFS= read -r line; do
    # Ignora linhas vazias e comentários
    if [[ -z "$line" || "$line" =~ ^# ]]; then
        continue
    fi

    TARGET_PATH="$TARGET_DIR/$line"

    # Diretório (termina com "/")
    if [[ "$line" == */ ]]; then
        mkdir -p "$TARGET_PATH"
        echo "Criado diretório: $TARGET_PATH"
    else
        # Arquivo
        DIR=$(dirname "$TARGET_PATH")
        mkdir -p "$DIR"
        touch "$TARGET_PATH"
        echo "Criado arquivo: $TARGET_PATH"
    fi

done < "$CONFIG_FILE"

echo ""
echo "Estrutura criada com sucesso!"
echo ""

###############################################################################
# 2. Criar e configurar ambiente Python com pyenv
###############################################################################

# Nome da pasta principal do projeto
PROJECT_NAME="$(basename "$TARGET_DIR")"

PYTHON_VERSION="3.12"

echo "Configurando ambiente Python para o projeto: $PROJECT_NAME"
echo "Versão do Python: $PYTHON_VERSION"
echo ""

# Instalar Python caso não exista
if ! pyenv versions --bare | grep -q "$PYTHON_VERSION"; then
    echo "Python $PYTHON_VERSION não encontrado. Instalando via pyenv..."
    pyenv install "$PYTHON_VERSION"
else
    echo "Python $PYTHON_VERSION já está instalado no pyenv."
fi

# Criar virtualenv com o nome do projeto
echo "Criando ambiente virtual: $PROJECT_NAME"
pyenv virtualenv "$PYTHON_VERSION" "$PROJECT_NAME"

# Criar arquivo .python-version na raiz do projeto
echo "$PROJECT_NAME" > "$TARGET_DIR/.python-version"
echo "Criado arquivo .python-version para ativação automática via pyenv."

###############################################################################
# 3. Ativação automática com direnv (opcional, recomendada)
###############################################################################

# Criar .envrc com ativação automática
ENVRC_FILE="$TARGET_DIR/.envrc"

if [[ ! -f "$ENVRC_FILE" ]]; then
    echo "Criando arquivo .envrc para ativação automática (direnv)..."
    cat <<EOF > "$ENVRC_FILE"
# Ativa automaticamente o ambiente virtual pyenv do projeto
layout python $(pyenv root)/versions/$PROJECT_NAME/bin/python
EOF
else
    echo ".envrc já existe — não sobrescrito."
fi

echo ""
echo "Para ativar o direnv, execute dentro da pasta do projeto:"
echo "  direnv allow"
echo ""

echo "Ambiente Python configurado com sucesso!"
echo "Ambiente virtual: $PROJECT_NAME"
