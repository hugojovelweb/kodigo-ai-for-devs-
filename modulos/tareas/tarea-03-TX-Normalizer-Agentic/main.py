#!/usr/bin/env python3
"""
main.py
-------
Punto de entrada.

    python main.py [ruta_transacciones.json] [ruta_rules.json]
    python main.py --classic [ruta_transacciones.json] [ruta_rules.json]

Por defecto se ejecuta el agente conversacional (src/cli.py). La bandera
--classic conserva la interfaz de menús previa a la refactorización
(src/classic_menu.py), útil para comparar el comportamiento antes/después.

Requiere ANTHROPIC_API_KEY en el entorno para operar el agente en modo
ONLINE (tool use real). Sin esa variable, el agente opera en modo
OFFLINE con un enrutador determinístico equivalente, documentado en el
README.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    if "--classic" in sys.argv:
        sys.argv.remove("--classic")
        from classic_menu import main
    else:
        from cli import main

    main()
