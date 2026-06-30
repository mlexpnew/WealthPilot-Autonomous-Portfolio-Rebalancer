from core.base_agent import BaseAgent
from core.state import PortfolioState


class ConfidenceAgent(BaseAgent):

    def __init__(self):
        super().__init__("ConfidenceAgent")

    def execute(self, state: PortfolioState):

        confidence = 100

        confidence -= state.drift * 150

        if state.risk_score > 1:
            confidence -= 10

        if state.tax_estimate > 1000:
            confidence -= 5

        confidence = max(50, min(99, int(confidence)))

        state.confidence_score = confidence

        return state