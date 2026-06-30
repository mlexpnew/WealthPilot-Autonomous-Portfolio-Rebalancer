from core.base_agent import BaseAgent
from core.state import PortfolioState
from services.decision_engine import DecisionEngine


class DecisionAgent(BaseAgent):

    def __init__(self):
        super().__init__("DecisionAgent")
        self.engine = DecisionEngine()

    def execute(self, state: PortfolioState) -> PortfolioState:

        self.log("Evaluating Rebalancing Decision")

        volatility = (
            state.market_data.get("volatility", 0.0) * 100
        )

        result = self.engine.evaluate(
            drift=state.drift * 100,
            risk_score=state.risk_score,
            volatility=volatility,
            calendar_due=False,
            market_event=False,
        )

        state.decision_score = result.score
        state.decision_reasons = result.reasons

        if result.should_rebalance:
            state.trigger = "REBALANCE"
        else:
            state.trigger = "HOLD"

        self.log(f"Decision Score : {state.decision_score}")
        self.log(f"Decision : {state.trigger}")

        return state