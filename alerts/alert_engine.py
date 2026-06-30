from datetime import datetime


class AlertEngine:

    def generate(self, state):

        alerts = []

        if state.drift >= 0.05:

            alerts.append({
                "severity": "High",
                "title": "Portfolio Drift",
                "message": f"Portfolio drift reached {state.drift*100:.2f}%.",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

        if state.risk_score > 1.0:

            alerts.append({
                "severity": "Medium",
                "title": "High Risk",
                "message": f"Risk score is {state.risk_score:.2f}.",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

        if state.tax_estimate > 500:

            alerts.append({
                "severity": "Low",
                "title": "Tax Impact",
                "message": f"Estimated tax ₹{state.tax_estimate:,.0f}.",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

        return alerts