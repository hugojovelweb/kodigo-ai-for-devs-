"""
validator.py
------------  ### Hugo Ernesto Jovel Hernandez
Responsabilidad ÚNICA: aplicar las reglas de validez de negocio sobre
transacciones YA normalizadas (no sobre el registro crudo).

Política de manejo de inválidas (decisión explícita del desarrollador,
documentada en config/rules.json -> politica_validacion):
    -> Las transacciones inválidas NO se descartan.
    -> Se separan en una lista aparte junto con el/los motivo(s),
       para permitir auditoría y trazabilidad posterior.
"""

from typing import List, Tuple
from models import NormalizedTransaction, InvalidTransaction


class TransactionValidator:
    def __init__(self, rules: dict):
        self.rules = rules
        self.valid_currencies = set(rules["monedas_soportadas"]["codigos_validos"])
        self.valid_statuses = {"SUCCESS", "FAILED", "PENDING"}

    def validate(self, tx: NormalizedTransaction) -> List[str]:
        """Devuelve una lista de motivos de invalidez. Lista vacía => válida."""
        reasons = []

        if not tx.id:
            reasons.append("id_normalizado vacío")

        if tx.amount is None or tx.amount <= 0:
            reasons.append(f"monto inválido (debe ser > 0): {tx.amount}")

        if tx.currency not in self.valid_currencies:
            reasons.append(f"moneda no soportada: {tx.currency}")

        if tx.status not in self.valid_statuses:
            reasons.append(f"estado normalizado no reconocido: {tx.status}")

        if not tx.timestamp or "T" not in tx.timestamp:
            reasons.append(f"timestamp con formato no ISO-8601: {tx.timestamp}")

        return reasons

    def split(
        self, normalized: List[NormalizedTransaction]
    ) -> Tuple[List[NormalizedTransaction], List[InvalidTransaction]]:
        """Separa una lista de transacciones normalizadas en válidas / inválidas."""
        valid, invalid = [], []
        for tx in normalized:
            reasons = self.validate(tx)
            if reasons:
                invalid.append(InvalidTransaction(original_record=tx.to_dict(), source=tx.source, reasons=reasons))
            else:
                valid.append(tx)
        return valid, invalid
