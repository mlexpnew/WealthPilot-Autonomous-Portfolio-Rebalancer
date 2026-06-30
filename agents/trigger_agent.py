from datetime import datetime

from config.settings import settings
from core.base_agent import BaseAgent
from core.state import PortfolioState


class TriggerAgent(BaseAgent):

    def __init__(self):
        super().__init__("TriggerAgent")

    def execute(self, state: PortfolioState) -> PortfolioState:

        self.log("Checking Rebalancing Trigger")

        if state.drift >= settings.DRIFT_THRESHOLD:

            state.trigger = "THRESHOLD"

        else:

            month = datetime.now().month

            if month in [3, 6, 9, 12]:

                state.trigger = "CALENDAR"

            else:

                state.trigger = "NONE"

        self.log(f"Trigger = {state.trigger}")

        return state