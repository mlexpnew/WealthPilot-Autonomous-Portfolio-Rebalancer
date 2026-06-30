from typing import List

from tax.tax_lot import TaxLot


class TaxOptimizer:

    """
    Minimize tax before generating sell orders.
    """

    def choose_lots_to_sell(
        self,
        lots: List[TaxLot],
        quantity: float,
    ) -> List[TaxLot]:

        remaining = quantity

        selected = []

        lots = sorted(

            lots,

            key=lambda x: (

                not x.is_long_term,

                x.gain,

            )

        )

        for lot in lots:

            if remaining <= 0:
                break

            selected.append(lot)

            remaining -= lot.quantity

        return selected

    def estimate_tax(self, lots: List[TaxLot]):

        tax = 0

        for lot in lots:

            if lot.gain <= 0:
                continue

            if lot.is_long_term:

                tax += lot.gain * 0.125

            else:

                tax += lot.gain * 0.20

        return round(tax, 2)