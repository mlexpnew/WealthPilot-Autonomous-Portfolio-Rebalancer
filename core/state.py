from typing import Any

from pydantic import BaseModel, Field


class PortfolioState(BaseModel):
    portfolio_id: str
    client_name: str
    risk_category: str

    current_allocation: dict[str, float]
    target_allocation: dict[str, float]

    portfolio_value: float = 1_000_000.0

    drift: float = 0.0
    trigger: str = "NONE"

    market_data: dict[str, Any] = Field(default_factory=dict)

    risk_score: float = 0.0

    tax_estimate: float = 0.0

    trade_list: list[dict[str, Any]] = Field(default_factory=list)

    explanation: dict[str, Any] = Field(default_factory=dict)

    compliance_status: bool = False

    approved: bool = False

    decision_score: float = 0.0

    decision_reasons: list[str] = Field(default_factory=list)
    
    confidence_score: int = 0
    
    execution_timeline: dict = {}