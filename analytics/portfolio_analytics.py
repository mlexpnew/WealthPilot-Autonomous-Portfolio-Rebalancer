from pathlib import Path
import json


class PortfolioAnalytics:

    def __init__(self):

        self.file = Path(
            "audit_logs/audit_history.json"
        )

    def summary(self):

        if not self.file.exists():

            return {}

        with open(self.file) as f:

            history = json.load(f)

        if len(history) == 0:

            return {}

        avg_drift = sum(
            x["drift"] for x in history
        ) / len(history)

        avg_risk = sum(
            x["risk_score"] for x in history
        ) / len(history)

        avg_tax = sum(
            x["tax"] for x in history
        ) / len(history)

        approvals = sum(
            1 for x in history if x["approved"]
        )

        rebalances = sum(
            1
            for x in history
            if x["trigger"] == "REBALANCE"
        )

        return {

            "total_decisions": len(history),

            "rebalances": rebalances,

            "approval_rate":
                round(
                    approvals
                    / len(history)
                    * 100,
                    2,
                ),

            "average_drift":
                round(avg_drift, 4),

            "average_risk":
                round(avg_risk, 2),

            "average_tax":
                round(avg_tax, 2),
            "average_confidence":
                round(sum(x["confidence_score"] for x in history) / len(history), 2),
        }