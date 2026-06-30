from approval.approval_service import ApprovalService
from core.base_agent import BaseAgent
from core.state import PortfolioState


class ApprovalAgent(BaseAgent):

    def __init__(self):
        super().__init__("ApprovalAgent")
        self.service = ApprovalService()

    def execute(self, state: PortfolioState) -> PortfolioState:

        self.log("Processing approval workflow")

        approval = self.service.request(state)

        if state.decision_score >= 60:
            state = self.service.approve(state)
            approval["status"] = "APPROVED"

            self.log(
                f"Portfolio {state.portfolio_id} approved."
            )

        else:
            state = self.service.reject(state)
            approval["status"] = "REJECTED"

            self.log(
                f"Portfolio {state.portfolio_id} rejected."
            )

        if state.explanation is None:
            state.explanation = {}

        state.explanation["approval"] = approval

        return state