import numpy as np


class MonteCarloSimulator:

    def simulate(

        self,

        portfolio_value: float,

        years: int = 10,

        simulations: int = 500,

    ):

        annual_return = 0.12

        volatility = 0.18

        final_values = []

        for _ in range(simulations):

            value = portfolio_value

            for _ in range(years):

                growth = np.random.normal(

                    annual_return,

                    volatility,

                )

                value *= (1 + growth)

            final_values.append(round(value, 2))

        return {

            "expected": round(

                float(np.mean(final_values)),

                2,

            ),

            "best": round(

                float(max(final_values)),

                2,

            ),

            "worst": round(

                float(min(final_values)),

                2,

            ),

            "median": round(

                float(np.median(final_values)),

                2,

            ),

            "distribution": final_values,

        }