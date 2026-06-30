class LegacyStrategy:

    def run(self, portfolio):

        drift = 0.0

        for asset in portfolio.target_allocation:

            current = portfolio.current_allocation.get(asset, 0.0)
            target = portfolio.target_allocation.get(asset, 0.0)

            drift += abs(current - target)

        drift /= 2

        return {
            "rebalanced": drift >= 0.05,
            "turnover": round(drift, 4),
        }