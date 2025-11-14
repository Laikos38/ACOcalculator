#!/bin/bash
# Script para ejecutar ACOCalculator con uv

cd "$(dirname "$0")/.."
uv run python main.py "$@"

