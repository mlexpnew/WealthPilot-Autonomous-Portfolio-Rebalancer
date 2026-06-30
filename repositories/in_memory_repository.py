from repositories.portfolio_repository import PortfolioRepository
from core.state import PortfolioState


class InMemoryPortfolioRepository(
    PortfolioRepository
):

    def __init__(self):

        self.storage = {}

    def save(self, portfolio):

        self.storage[
            portfolio.portfolio_id
        ] = portfolio

    def get_portfolio(self, portfolio_id):

        return self.storage.get(portfolio_id)

    def list_portfolios(self):

        return list(self.storage.values())