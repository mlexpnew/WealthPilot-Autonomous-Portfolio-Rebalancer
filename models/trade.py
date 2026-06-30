from enum import Enum

from pydantic import BaseModel, Field


class TradeAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class Trade(BaseModel):
    symbol: str

    asset_class: str

    action: TradeAction

    current_weight: float

    target_weight: float

    weight_difference: float

    amount: float = Field(..., ge=0)

    quantity: float = Field(..., ge=0)

    price: float = Field(..., gt=0)

    reason: str