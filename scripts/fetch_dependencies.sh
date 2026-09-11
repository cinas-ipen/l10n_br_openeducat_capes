#!/usr/bin/env bash
set -e

# Diretório base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
EXTERNAL_ADDONS_DIR="$ROOT_DIR/external_addons"

echo "=== Verificando dependências externas do OpenEduCat ==="
mkdir -p "$EXTERNAL_ADDONS_DIR"

# Repositório oficial do OpenEduCat (Branch 19.0)
OPENEDUCAT_REPO="https://github.com/openeducat/openeducat_erp.git"
OPENEDUCAT_BRANCH="19.0"

if [ ! -d "$EXTERNAL_ADDONS_DIR/openeducat_core" ]; then
    echo "Clonando openeducat_erp (branch $OPENEDUCAT_BRANCH) em $EXTERNAL_ADDONS_DIR..."
    git clone --depth 1 --single-branch -b "$OPENEDUCAT_BRANCH" "$OPENEDUCAT_REPO" "$EXTERNAL_ADDONS_DIR/temp_openeducat" || {
        echo "Aviso: Falha ao clonar branch $OPENEDUCAT_BRANCH. Tentando branch master/main..."
        git clone --depth 1 "$OPENEDUCAT_REPO" "$EXTERNAL_ADDONS_DIR/temp_openeducat"
    }
    
    # Copiar/Mover módulos de openeducat para external_addons
    if [ -d "$EXTERNAL_ADDONS_DIR/temp_openeducat" ]; then
        echo "Organizando módulos do OpenEduCat..."
        cp -r "$EXTERNAL_ADDONS_DIR/temp_openeducat"/* "$EXTERNAL_ADDONS_DIR/" 2>/dev/null || true
        rm -rf "$EXTERNAL_ADDONS_DIR/temp_openeducat"
    fi
    echo "Dependências do OpenEduCat instaladas com sucesso em external_addons!"
else
    echo "Dependência 'openeducat_core' já encontrada em $EXTERNAL_ADDONS_DIR."
fi

echo "=== Dependências verificadas ==="
