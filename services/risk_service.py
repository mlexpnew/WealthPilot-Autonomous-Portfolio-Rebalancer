import numpy as np


class RiskService:

    def volatility(self, returns):

        return float(np.std(returns))

    def downside_risk(self, returns):

        downside = [

            x

            for x in returns

            if x < 0

        ]

        if len(downside) == 0:

            return 0

        return float(np.std(downside))

    def max_drawdown(self, prices):

        prices = np.array(prices)

        cumulative = prices / prices[0]

        running_max = np.maximum.accumulate(
            cumulative
        )

        drawdown = (
            cumulative - running_max
        ) / running_max

        return float(drawdown.min())