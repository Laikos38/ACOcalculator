#!/bin/bash
# Script para verificar la instalación de ACOCalculator con uv

cd "$(dirname "$0")/.."
uv run python verify_installation.py "$@"

