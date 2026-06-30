from datetime import datetime

from pydantic import BaseModel


class MarketSnapshot(BaseModel):

    timestamp: datetime

    nifty: float

    bank_nifty: float

    india_vix: float

    market_sentiment: str

    volatility: float

    regime: str