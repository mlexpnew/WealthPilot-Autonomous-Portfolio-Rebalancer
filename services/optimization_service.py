import cvxpy as cp
import numpy as np


class PortfolioOptimizer:

    def optimize(
        self,
        expected_returns,
        covariance,
    ):

        n = len(expected_returns)

        weights = cp.Variable(n)

        objective = cp.Maximize(

            expected_returns @ weights

        )

        constraints = [

            cp.sum(weights) == 1,

            weights >= 0,

        ]

        problem = cp.Problem(

            objective,

            constraints,

        )

        problem.solve()

        return np.round(

            weights.value,

            4,

        )