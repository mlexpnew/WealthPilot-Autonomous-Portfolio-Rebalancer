import numpy as np


class BacktestMetrics:

    @staticmethod
    def annual_return(returns):
        returns = np.asarray(returns)
        if len(returns) == 0:
            return 0.0
        return round(((1 + returns).prod() ** (252 / len(returns)) - 1) * 100, 2)

    @staticmethod
    def volatility(returns):
        returns = np.asarray(returns)
        return round(np.std(returns) * np.sqrt(252) * 100, 2)

    @staticmethod
    def sharpe(returns, rf=0.06):
        returns = np.asarray(returns)

        if len(returns) == 0:
            return 0.0

        excess = returns - rf / 252

        std = np.std(excess)

        if std == 0:
            return 0.0

        return round(np.mean(excess) / std * np.sqrt(252), 2)

    @staticmethod
    def max_drawdown(cumulative):

        cumulative = np.asarray(cumulative)

        running_max = np.maximum.accumulate(cumulative)

        drawdown = (cumulative - running_max) / running_max

        return round(drawdown.min() * 100, 2)