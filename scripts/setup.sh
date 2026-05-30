#!/bin/bash
set -e

VAULT_PATH="${1:-.}"
DOMAIN_DIR="${2:-general}"

echo "Creating vault structure in $VAULT_PATH..."

# Core directories
mkdir -p "$VAULT_PATH/00_CORE/identity"
mkdir -p "$VAULT_PATH/00_CORE/stakeholders"
mkdir -p "$VAULT_PATH/00_CORE/strategy"
mkdir -p "$VAULT_PATH/10_PEOPLE"
mkdir -p "$VAULT_PATH/20_MEETINGS/committees"
mkdir -p "$VAULT_PATH/20_MEETINGS/sessions"
mkdir -p "$VAULT_PATH/20_MEETINGS/standups"
mkdir -p "$VAULT_PATH/30_PROJECTS/active"
mkdir -p "$VAULT_PATH/30_PROJECTS/backlog"
mkdir -p "$VAULT_PATH/30_PROJECTS/archive"
mkdir -p "$VAULT_PATH/40_DECISIONS/records"
mkdir -p "$VAULT_PATH/40_DECISIONS/policies"
mkdir -p "$VAULT_PATH/40_DECISIONS/journal"
mkdir -p "$VAULT_PATH/50_KNOWLEDGE/methodology"
mkdir -p "$VAULT_PATH/50_KNOWLEDGE/processes"
mkdir -p "$VAULT_PATH/50_KNOWLEDGE/glossary"
mkdir -p "$VAULT_PATH/60_DOMAIN/$DOMAIN_DIR"
mkdir -p "$VAULT_PATH/90_TEMPLATES"
mkdir -p "$VAULT_PATH/99_ARCHIVE/transcripts"
mkdir -p "$VAULT_PATH/99_ARCHIVE/projects"

echo "✓ Vault structure created ($(find "$VAULT_PATH" -type d | wc -l | tr -d ' ') directories)"
