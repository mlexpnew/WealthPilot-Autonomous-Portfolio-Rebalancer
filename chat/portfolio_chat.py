from typing import Dict


class PortfolioChat:

    def reply(

        self,

        question: str,

        portfolio: Dict,

    ) -> str:

        q = question.lower()

        if "risk" in q:

            return (
                f"Current Risk Score is "
                f"{portfolio['risk_score']:.2f}."
            )

        if "drift" in q:

            return (
                f"Portfolio Drift is "
                f"{portfolio['drift']*100:.2f}%."
            )

        if "rebalance" in q:

            return (
                portfolio["explanation"]["client"]
            )

        if "tax" in q:

            return (
                f"Estimated Tax Impact is "
                f"₹{portfolio['tax_estimate']:,.0f}."
            )

        if "trade" in q:

            if len(portfolio["trade_list"]) == 0:

                return "No trades are required."

            text = "Recommended Trades:\n\n"

            for trade in portfolio["trade_list"]:

                text += (
                    f"{trade['action']} "
                    f"{trade['symbol']} "
                    f"₹{trade['amount']:,.0f}\n"
                )

            return text

        if "decision" in q:

            return (
                f"Decision Score : "
                f"{portfolio['decision_score']}"
            )

        if "approval" in q:

            if portfolio["approved"]:

                return "Portfolio has been approved."

            return "Portfolio is pending approval."

        return (
            "I can answer questions about "
            "risk, drift, trades, tax, "
            "approval and rebalancing."
        )