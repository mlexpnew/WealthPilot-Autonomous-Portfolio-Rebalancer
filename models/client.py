from enum import Enum

# Prefer pydantic when available, but provide lightweight fallbacks so editors
# / linters that can't resolve pydantic won't break the module.
try:
    from pydantic import BaseModel, Field
except Exception:  # pragma: no cover - fallback for environments without pydantic
    from typing import Any

    def Field(*, default: Any = None, **kwargs: Any) -> Any:
        return default

    class BaseModel:  # very small runtime-compatible fallback
        def __init__(self, **data: Any) -> None:
            for k, v in data.items():
                setattr(self, k, v)

        def dict(self) -> dict:
            return {k: getattr(self, k) for k in self.__dict__}


class RiskCategory(str, Enum):
    CONSERVATIVE = "Conservative"
    MODERATE = "Moderate"
    AGGRESSIVE = "Aggressive"
    VERY_AGGRESSIVE = "Very Aggressive"
    RETIREMENT = "Retirement"


class Client(BaseModel):
    client_id: str  

    name: str

    risk_category: RiskCategory

    portfolio_value: float = Field(gt=0)

    tax_rate: float = Field(default=0.20)

    cash_available: float = Field(default=0)

    rebalance_allowed: bool = True