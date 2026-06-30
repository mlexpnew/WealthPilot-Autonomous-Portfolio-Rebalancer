from core.base_agent import BaseAgent
from core.state import PortfolioState

from market.market_data import MarketDataService
from risk.risk_metrics import RiskCalculator


class RiskAgent(BaseAgent):

    def __init__(self):

        super().__init__("RiskAgent")

        self.market = MarketDataService()

    def execute(self, state: PortfolioState):

        self.log("Calculating Portfolio Risk")

        returns = self.market.get_returns("^NSEI")

        volatility = RiskCalculator.volatility(returns)

        sharpe = RiskCalculator.sharpe_ratio(returns)

        var = RiskCalculator.value_at_risk(returns)

        state.risk_score = round(volatility * 100, 2)

        state.market_data["volatility"] = volatility

        state.market_data["sharpe"] = sharpe

        state.market_data["var95"] = var

        self.log(
            f"Volatility={volatility:.4f} "
            f"Sharpe={sharpe:.4f} "
            f"VaR={var:.4f}"
        )

        return state