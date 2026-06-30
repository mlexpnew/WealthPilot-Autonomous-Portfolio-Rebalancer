from agents.orchestrator import Orchestrator


class AgentStrategy:

    def __init__(self):

        self.agent = Orchestrator()

    def run(self, portfolio):

        state = self.agent.run(portfolio)

        return {
            "rebalanced": state.trigger == "REBALANCE",
            "turnover": state.drift,
            "tax": state.tax_estimate,
            "decision_score": state.decision_score,
        }