class AdvisorExplainer:

    def generate(self, state):

        return {

            "trigger": state.trigger,

            "portfolio_drift": state.drift,

            "risk_score": state.risk_score,

            "tax": state.tax_estimate,

            "number_of_trades": len(state.trade_list),

            "compliance": state.compliance_status,

        }