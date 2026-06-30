from compliance.checker import ComplianceChecker

from core.base_agent import BaseAgent


class ComplianceAgent(BaseAgent):

    def __init__(self):

        super().__init__("ComplianceAgent")

        self.engine = ComplianceChecker()

    def execute(self, state):

        self.log("Running Compliance Checks")

        errors = self.engine.validate(state)

        if errors:

            self.log("Compliance Failed")

            for error in errors:

                self.log(error)

        else:

            self.log("Compliance Passed")

        return state