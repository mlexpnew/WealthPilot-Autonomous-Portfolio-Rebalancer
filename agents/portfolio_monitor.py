from core.base_agent import BaseAgent
from core.state import PortfolioState
from services.drift_service import DriftService


class PortfolioMonitorAgent(BaseAgent):
    def __init__(self):
        super().__init__("PortfolioMonitor")
        self.drift_service = DriftService()

    def execute(self, state: PortfolioState) -> PortfolioState:
        self.log(f"Monitoring Portfolio {state.portfolio_id}")

        result = self.drift_service.calculate(
            current=state.current_allocation,
            target=state.target_allocation,
        )

        state.drift = result["turnover"]

        self.log(f"Portfolio Drift : {state.drift:.2%}")

        return state