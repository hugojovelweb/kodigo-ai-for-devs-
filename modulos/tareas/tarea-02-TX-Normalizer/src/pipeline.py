"""
pipeline.py
-----------  ### Hugo Ernesto Jovel Hernandez
Orquesta el flujo completo: carga de archivos -> normalización ->
validación -> métricas. No contiene reglas de negocio propias; delega
en normalizer.py, validator.py y metrics.py.
"""

from typing import List, Tuple
from loader import load_transactions, load_rules
from normalizer import TransactionNormalizer
from validator import TransactionValidator
from metrics import MetricsCalculator
from models import NormalizedTransaction, InvalidTransaction


class Pipeline:
    def __init__(self, data_path: str, rules_path: str):
        self.data_path = data_path
        self.rules_path = rules_path
        self.rules = load_rules(rules_path)
        self.normalizer = TransactionNormalizer(self.rules)
        self.validator = TransactionValidator(self.rules)

        self.raw_records: List[dict] = []
        self.valid: List[NormalizedTransaction] = []
        self.invalid: List[InvalidTransaction] = []  # inválidas por normalización O por validación
        self.metrics: dict = {}

    def run(self) -> None:
        self.raw_records = load_transactions(self.data_path)

        normalized_ok: List[NormalizedTransaction] = []

        # Paso 1: normalización (detección de fuente + transformación de formato)
        for record in self.raw_records:
            tx, errors = self.normalizer.normalize(record)
            if tx is None:
                self.invalid.append(
                    InvalidTransaction(
                        original_record=record,
                        source=self.normalizer.detect_source(record) or "desconocida",
                        reasons=errors,
                    )
                )
            else:
                normalized_ok.append(tx)

        # Paso 2: validación de negocio sobre lo ya normalizado
        valid, invalid_by_rules = self.validator.split(normalized_ok)
        self.valid = valid
        self.invalid.extend(invalid_by_rules)

        # Paso 3: métricas
        calc = MetricsCalculator(self.valid, self.invalid, total_raw=len(self.raw_records))
        self.metrics = calc.summary()

    def reload(self) -> None:
        self.valid.clear()
        self.invalid.clear()
        self.metrics.clear()
        self.run()
