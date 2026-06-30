from core.base_agent import BaseAgent

from explanations.client import ClientExplainer
from explanations.advisor import AdvisorExplainer
from explanations.compliance import ComplianceExplainer


class ExplanationAgent(BaseAgent):

    def __init__(self):

        super().__init__("ExplanationAgent")

        self.client = ClientExplainer()

        self.advisor = AdvisorExplainer()

        self.compliance = ComplianceExplainer()

    def execute(self, state):

        self.log("Generating explanations")

        state.explanation = {

            "client": self.client.generate(state),

            "advisor": self.advisor.generate(state),

            "compliance": self.compliance.generate(state),

        }

        return state