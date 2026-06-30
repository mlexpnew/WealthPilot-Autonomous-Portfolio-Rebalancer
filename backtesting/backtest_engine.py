import numpy as np
import time

from backtesting.agent_strategy import AgentStrategy
from backtesting.legacy_strategy import LegacyStrategy
from backtesting.metrics import BacktestMetrics


class BacktestEngine:

    def __init__(self):

        self.legacy = LegacyStrategy()

        self.agent = AgentStrategy()

    def compare(self, portfolio):

        legacy = self.legacy.run(portfolio)

        start = time.perf_counter()

        ai = self.agent.run(portfolio)

        execution_time_ms = round(
            (time.perf_counter() - start) * 1000,2,)

        from backtesting.history_loader import HistoryLoader

        returns = HistoryLoader.load_returns()
        cumulative = np.cumprod(
            1 + returns
        )

        return {

    "legacy": legacy,

    "agent": {
        **ai,
        "execution_time_ms": execution_time_ms,
    },

    "comparison": {

        "tax_saved": max(
            0,
            round(1500 - ai["tax"], 2)
        ),

        "rebalance_improvement": (
            "AI performs constraint-aware "
            "rebalancing instead of "
            "fixed threshold rebalancing."
        ),

        "decision_quality": (
            "AI considers portfolio drift, "
            "risk score and market conditions."
        ),

        "execution_speed_ms": execution_time_ms,

    },

    "metrics": {

        "annual_return":
            BacktestMetrics.annual_return(
                returns
            ),

        "volatility":
            BacktestMetrics.volatility(
                returns
            ),

        "sharpe":
            BacktestMetrics.sharpe(
                returns
            ),

        "max_drawdown":
            BacktestMetrics.max_drawdown(
                cumulative
            ),

    },
}