#!/bin/bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

success() { echo -e "${GREEN}✓${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1" >&2; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
info() { echo -e "→ $1"; }

install_qmd() {
    info "Installing qmd..."
    if command -v qmd &>/dev/null; then
        success "qmd already installed ($(qmd --version 2>/dev/null || echo 'unknown version'))"
        return 0
    fi
    if ! command -v node &>/dev/null; then
        error "Node.js not found. Install Node.js 18+ first: https://nodejs.org"
        return 1
    fi
    npm install -g @tobilu/qmd
    if command -v qmd &>/dev/null; then
        success "qmd installed ($(qmd --version))"
    else
        error "qmd installation failed"
        return 1
    fi
}

install_tg_parser() {
    info "Installing tg-parser..."
    if command -v tg-parser &>/dev/null; then
        success "tg-parser already installed"
        return 0
    fi
    if command -v uv &>/dev/null; then
        uv tool install tg-parser
    elif command -v pip3 &>/dev/null; then
        pip3 install tg-parser
    else
        error "Neither uv nor pip3 found. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
        return 1
    fi
    success "tg-parser installed"
}

echo ""
echo "=== Executive Assistant — Tool Installer ==="
echo ""

# Parse arguments
INSTALL_QMD=false
INSTALL_TG=false

for arg in "$@"; do
    case $arg in
        --qmd) INSTALL_QMD=true ;;
        --tg-parser) INSTALL_TG=true ;;
        --all) INSTALL_QMD=true; INSTALL_TG=true ;;
        --help) echo "Usage: $0 [--qmd] [--tg-parser] [--all]"; exit 0 ;;
    esac
done

if [ "$INSTALL_QMD" = true ]; then
    install_qmd || true
fi

if [ "$INSTALL_TG" = true ]; then
    install_tg_parser || true
fi

echo ""
echo "=== Done ==="
