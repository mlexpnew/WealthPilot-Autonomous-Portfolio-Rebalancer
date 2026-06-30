from core.base_agent import BaseAgent
from core.state import PortfolioState


class HumanOverrideAgent(BaseAgent):

    def __init__(self):
        super().__init__("HumanOverrideAgent")

    def execute(
        self,
        state: PortfolioState,
        action: str = "AUTO",
    ) -> PortfolioState:

        self.log(f"Override Action : {action}")

        if action == "APPROVE":

            state.approved = True

            state.decision_reasons.append(
                "Approved by Human Advisor."
            )

        elif action == "REJECT":

            state.approved = False

            state.trade_list = []

            state.decision_reasons.append(
                "Rejected by Human Advisor."
            )

        elif action == "MODIFY":

            state.decision_reasons.append(
                "Trade list modified by Human Advisor."
            )

        return state