from core.base_agent import BaseAgent
from core.state import PortfolioState

from optimizer.trade_optimizer import TradeOptimizer
from services.price_service import PriceService


class TradeAgent(BaseAgent):

    def __init__(self):

        super().__init__("TradeAgent")

        self.optimizer = TradeOptimizer()

    def execute(self, state: PortfolioState):

        self.log("Generating Trade List")

        symbols = [

            "NIFTYBEES.NS",

            "LIQUIDBEES.NS",

            "GOLDBEES.NS",

        ]

        prices = PriceService.get_prices(symbols)

        trades = self.optimizer.generate_trades(

            portfolio_value=1000000,

            current=state.current_allocation,

            target=state.target_allocation,

            prices=prices,

        )

        state.trade_list = [

            trade.model_dump()

            for trade in trades

        ]

        self.log(f"{len(trades)} trades generated")

        return state