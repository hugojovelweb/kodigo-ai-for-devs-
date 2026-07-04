#!/usr/bin/env python3   by Hugo Ernesto Jovel Hernandez
"""
main.py
-------
Punto de entrada. Ejecutar con:

    python main.py [ruta_transacciones.json] [ruta_rules.json]

Por defecto usa data/transacciones.json y config/rules.json.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from cli import main  # noqa: E402

if __name__ == "__main__":
    main()
