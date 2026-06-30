class PortfolioComparison:

    def compare(
        self,
        p1: dict,
        p2: dict,
    ):

        return {

            "portfolio_1": {

                "id": p1["portfolio_id"],

                "client": p1["client_name"],

                "risk_score": p1["risk_score"],

                "decision_score": p1["decision_score"],

                "drift": p1["drift"],

                "tax": p1["tax_estimate"],

                "approved": p1["approved"],

            },

            "portfolio_2": {

                "id": p2["portfolio_id"],

                "client": p2["client_name"],

                "risk_score": p2["risk_score"],

                "decision_score": p2["decision_score"],

                "drift": p2["drift"],

                "tax": p2["tax_estimate"],

                "approved": p2["approved"],

            },

            "winner": {

                "lower_risk":

                    p1["client_name"]

                    if p1["risk_score"] < p2["risk_score"]

                    else p2["client_name"],

                "lower_tax":

                    p1["client_name"]

                    if p1["tax_estimate"] < p2["tax_estimate"]

                    else p2["client_name"],

                "higher_score":

                    p1["client_name"]

                    if p1["decision_score"] > p2["decision_score"]

                    else p2["client_name"],

            },

        }