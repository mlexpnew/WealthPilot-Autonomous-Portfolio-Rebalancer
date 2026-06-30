from datetime import datetime
from uuid import uuid4

from core.state import PortfolioState


class ApprovalService:

    def request(
        self,
        state: PortfolioState,
    ) -> dict:

        return {
            "approval_id": str(uuid4()),
            "requested_at": datetime.utcnow().isoformat(),
            "status": "PENDING",
            "portfolio_id": state.portfolio_id,
            "decision_score": state.decision_score,
            "trigger": state.trigger,
        }

    def approve(
        self,
        state: PortfolioState,
    ) -> PortfolioState:

        state.approved = True
        return state

    def reject(
        self,
        state: PortfolioState,
    ) -> PortfolioState:

        state.approved = False
        return state