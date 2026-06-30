import json
from pathlib import Path


class DecisionAnalytics:

    def __init__(self):

        self.file = Path("audit_logs/audit_history.json")

    def summary(self):

        if not self.file.exists():

            return {}

        with open(self.file) as f:

            history = json.load(f)

        if len(history) == 0:

            return {}

        total = len(history)

        approved = sum(
            1
            for h in history
            if h["approved"]
        )

        avg_score = round(

            sum(
                h["decision_score"]
                for h in history
            ) / total,

            2,

        )

        avg_tax = round(

            sum(
                h["tax"]
                for h in history
            ) / total,

            2,

        )

        avg_drift = round(

            sum(
                h["drift"]
                for h in history
            ) / total,

            4,

        )

        avg_risk = round(

            sum(
                h["risk_score"]
                for h in history
            ) / total,

            2,

        )

        return {

            "total_decisions": total,

            "approved": approved,

            "rejected": total - approved,

            "approval_rate":

                round(
                    approved * 100 / total,
                    2,
                ),

            "average_decision_score":

                avg_score,

            "average_tax":

                avg_tax,

            "average_drift":

                avg_drift,

            "average_risk_score":

                avg_risk,

        }