from datetime import datetime
import uuid


class ComplianceExplainer:

    def generate(self, state):

        return {

            "decision_id": str(uuid.uuid4()),

            "timestamp": datetime.utcnow().isoformat(),

            "trigger": state.trigger,

            "portfolio_drift": state.drift,

            "risk_score": state.risk_score,

            "tax": state.tax_estimate,

            "trade_count": len(state.trade_list),

            "approved": state.compliance_status,

        }