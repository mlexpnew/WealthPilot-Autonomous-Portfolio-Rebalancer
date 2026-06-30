import json
from pathlib import Path

from repositories.portfolio_repository import (
    PortfolioRepository,
)


class PortfolioService:

    def __init__(

        self,

        repository,

    ):

        self.repository = repository

    def portfolio_value(

        self,

        portfolio,

    ):

        total = 0

        for holding in portfolio.holdings:

            total += (

                holding.quantity

                * holding.current_price

            )

        return total

    def asset_weights(

        self,

        portfolio,

    ):

        total = self.portfolio_value(

            portfolio

        )

        allocation = {}

        for holding in portfolio.holdings:

            value = (

                holding.quantity

                * holding.current_price

            )

            allocation.setdefault(

                holding.asset_class,

                0,

            )

            allocation[holding.asset_class] += value

        for key in allocation:

            allocation[key] /= total

        return allocation
    
    
    import json
    from pathlib import Path
    def load_sample_portfolios(self):

        file = Path("data/clients.json")

        if not file.exists():
            return []

        with open(file, "r") as f:
            return json.load(f)

    def get_sample_portfolio(
        self,
        portfolio_id: str,
    ):

        portfolios = self.load_sample_portfolios()

        for portfolio in portfolios:

            if portfolio["portfolio_id"] == portfolio_id:
                return portfolio

        return None

    def get_by_risk(
        self,
        risk: str,
    ):

        portfolios = self.load_sample_portfolios()

        return [
            p
            for p in portfolios
            if p["risk_category"].lower()
            == risk.lower()
        ]