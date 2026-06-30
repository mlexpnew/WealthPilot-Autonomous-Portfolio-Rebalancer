import json
from datetime import datetime
from pathlib import Path

from core.base_agent import BaseAgent
from core.state import PortfolioState


class AuditAgent(BaseAgent):

    def __init__(self):
        super().__init__("AuditAgent")

        self.audit_file = Path("audit_logs/audit_history.json")

        self.audit_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def execute(
        self,
        state: PortfolioState,
    ) -> PortfolioState:

        self.log("Saving audit trail")

        record = {

            "timestamp": datetime.utcnow().isoformat(),

            "portfolio_id": state.portfolio_id,

            "client_name": state.client_name,

            "trigger": state.trigger,

            "decision_score": state.decision_score,

            "drift": state.drift,

            "risk_score": state.risk_score,

            "tax": state.tax_estimate,

            "approved": state.approved,

            "trade_count": len(state.trade_list),

            "trade_list": state.trade_list,

            "decision_reasons": state.decision_reasons,

        }

        history = []

        if self.audit_file.exists():

            try:

                with open(self.audit_file, "r") as f:
                    history = json.load(f)

            except Exception:
                history = []

        history.append(record)

        with open(self.audit_file, "w") as f:

            json.dump(
                history,
                f,
                indent=4,
                default=str,
            )

        return state