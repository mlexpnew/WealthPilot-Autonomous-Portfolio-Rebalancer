from sqlalchemy.orm import Session

from database.models import PortfolioORM


class PortfolioRepository:

    def __init__(self, db: Session):

        self.db = db

    def get(

        self,

        portfolio_code: str,

    ):

        return (

            self.db.query(

                PortfolioORM

            )

            .filter(

                PortfolioORM.portfolio_code

                == portfolio_code

            )

            .first()

        )

    def save(

        self,

        portfolio,

    ):

        self.db.add(portfolio)

        self.db.commit()

        self.db.refresh(portfolio)

        return portfolio