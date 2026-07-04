# Normalización y Exploración de Transacciones Multifuente 
  ### Hugo Ernesto Jovel Hernandez

Sistema en Python que lee transacciones provenientes de **3 fuentes distintas**
(cada una con su propio esquema), las **normaliza** a un formato común, las
**valida**, calcula **métricas** y permite **explorarlas mediante una CLI
interactiva** (menús, filtros, búsqueda, exportación).

## Requisitos

- Python 3.9+
- Sin dependencias externas (solo librería estándar)

## Ejecución

```bash
python main.py
```

Esto usa por defecto:
- Datos: `data/transacciones.json`
- Reglas: `config/rules.json`

También puedes indicar otros archivos:

```bash
python main.py data/transacciones_validas.json config/rules.json
```

## Estructura del proyecto

```
tx_normalizer/
├── main.py                        # Punto de entrada
├── config/
│   └── rules.json                 # Reglas: mapeo de estados, monedas, formatos de fecha
├── data/
│   ├── transacciones.json         # Dataset con casos válidos e inválidos (mezclados)
│   └── transacciones_validas.json # Dataset mayormente válido
├── src/
│   ├── models.py                  # Esquema normalizado (dataclasses)
│   ├── loader.py                  # Lectura de archivos JSON
│   ├── normalizer.py              # Detección de fuente + transformación de formato
│   ├── validator.py               # Reglas de validez de negocio
│   ├── metrics.py                 # Cálculo de métricas agregadas
│   ├── pipeline.py                # Orquestador: carga -> normaliza -> valida -> métricas
│   └── cli.py                     # Interfaz interactiva por menú
└── docs/
    └── nota_tecnica.docx          # Nota técnica de diseño y uso de IA
```

## Separación de responsabilidades

| Módulo | Responsabilidad |
|---|---|
| `loader.py` | Leer archivos del disco |
| `normalizer.py` | Detectar fuente y transformar al esquema común (montos, moneda, fecha) |
| `validator.py` | Aplicar reglas de validez de negocio sobre lo ya normalizado |
| `metrics.py` | Calcular métricas agregadas |
| `pipeline.py` | Orquestar el flujo completo |
| `cli.py` | Interfaz de usuario (menús, filtros, exportación) |

## Esquema normalizado

```json
{
  "id": "tx_001",
  "amount": 100.50,
  "currency": "USD",
  "timestamp": "2025-03-10T14:22:00Z",
  "status": "SUCCESS",
  "source": "source_a"
}
```

## Fuentes soportadas (detectadas automáticamente por sus campos)

| Fuente | Campos característicos | Particularidad |
|---|---|---|
| `source_a` | `id, amount, currency, timestamp, status` | Monto ya en decimal, fecha `YYYY-MM-DD HH:MM:SS` |
| `source_b` | `transaction_id, total, currency_code, created_at, state` | Monto en centavos (entero), fecha `DD/MM/YYYY HH:MM` |
| `source_c` | `ref, amount, date, result` | Monto con símbolo de moneda y coma decimal, fecha ISO-8601 nativa |

## Política de transacciones inválidas

Las transacciones que no pueden normalizarse o que no cumplen las reglas de
validez **no se descartan**: se separan en una lista de "inválidas" junto con
el/los motivo(s) del error, para permitir auditoría (ver menú "Ver
transacciones inválidas" y la exportación a JSON).

## Menú de la interfaz CLI

1. Ver todas las transacciones válidas
2. Filtrar por estado (SUCCESS / FAILED / PENDING)
3. Filtrar por moneda (con total agregado)
4. Buscar transacción por ID
5. Ver métricas generales
6. Ver transacciones inválidas (con motivo)
7. Exportar resultados normalizados a JSON
8. Recargar datos desde otro archivo

## Datos de prueba

- `data/transacciones.json`: incluye los 3 formatos de origen, con
  inconsistencias intencionales (id vacío, montos negativos o en cero,
  monto no numérico, moneda no soportada, fecha con formato incorrecto,
  estado desconocido, y un registro de fuente no reconocible).
- `data/transacciones_validas.json`: dataset mayormente válido para
  probar el flujo "feliz".
