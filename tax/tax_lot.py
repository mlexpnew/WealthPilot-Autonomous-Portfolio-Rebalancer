from datetime import date

from pydantic import BaseModel


class TaxLot(BaseModel):

    symbol: str

    quantity: float

    purchase_price: float

    current_price: float

    purchase_date: date

    @property
    def gain(self):

        return (
            self.current_price -
            self.purchase_price
        ) * self.quantity

    @property
    def holding_days(self):

        return (
            date.today() -
            self.purchase_date
        ).days

    @property
    def is_long_term(self):

        return self.holding_days >= 365