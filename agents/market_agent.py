from core.base_agent import BaseAgent
from core.state import PortfolioState
from market.market_data import MarketDataService
from market.event_detector import EventDetector

class MarketAgent(BaseAgent):

    def __init__(self):

        super().__init__("MarketAgent")

        self.market = MarketDataService()
        
        self.detector = EventDetector()

    def execute(self, state: PortfolioState):

        self.log("Fetching Live Market Data")

        snapshot = self.market.market_snapshot()

        state.market_data = snapshot

        self.log(snapshot)

        return state
        snapshot["market_event"] = self.detector.detect(
            snapshot
   )