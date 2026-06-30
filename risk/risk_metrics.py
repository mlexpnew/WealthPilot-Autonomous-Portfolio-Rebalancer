import numpy as np


class RiskCalculator:

    @staticmethod
    def volatility(returns):

        if len(returns) == 0:
            return 0

        return float(np.std(returns))

    @staticmethod
    def sharpe_ratio(
        returns,
        risk_free=0.06,
    ):

        if len(returns) == 0:
            return 0

        mean = np.mean(returns)

        std = np.std(returns)

        if std == 0:
            return 0

        return float((mean - risk_free / 252) / std)

    @staticmethod
    def value_at_risk(
        returns,
        confidence=95,
    ):

        if len(returns) == 0:
            return 0

        percentile = 100 - confidence

        return float(np.percentile(returns, percentile))