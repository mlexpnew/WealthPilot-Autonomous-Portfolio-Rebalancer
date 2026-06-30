from datetime import date

from core.base_agent import BaseAgent

from tax.tax_lot import TaxLot
from tax.tax_optimizer import TaxOptimizer


class TaxAgent(BaseAgent):

    def __init__(self):

        super().__init__("TaxAgent")

        self.optimizer = TaxOptimizer()

    def execute(self, state):

        self.log("Optimizing Tax")

        sample_lots = [

            TaxLot(

                symbol="NIFTYBEES.NS",

                quantity=100,

                purchase_price=210,

                current_price=260,

                purchase_date=date(2023, 5, 1),

            ),

            TaxLot(

                symbol="NIFTYBEES.NS",

                quantity=50,

                purchase_price=255,

                current_price=260,

                purchase_date=date(2026, 2, 10),

            ),

        ]

        selected = self.optimizer.choose_lots_to_sell(

            sample_lots,

            120,

        )

        state.tax_estimate = self.optimizer.estimate_tax(

            selected

        )

        self.log(

            f"Estimated Tax = ₹{state.tax_estimate}"

        )

        return state