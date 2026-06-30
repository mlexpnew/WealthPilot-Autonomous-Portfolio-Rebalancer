from datetime import datetime

from pydantic import BaseModel, Field


class Portfolio(BaseModel):

    portfolio_id: str

    client_id: str

    portfolio_value: float

    current_allocation: dict[str, float]

    target_allocation: dict[str, float]

    last_rebalanced: datetime

    created_at: datetime = Field(default_factory=datetime.utcnow)