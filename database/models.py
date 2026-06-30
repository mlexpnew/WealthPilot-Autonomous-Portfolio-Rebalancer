from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.base import Base


class ClientORM(Base):

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(

        Integer,

        primary_key=True,

    )

    client_code: Mapped[str] = mapped_column(

        String(20),

        unique=True,

    )

    name: Mapped[str]

    risk_category: Mapped[str]

    portfolios = relationship(

        "PortfolioORM",

        back_populates="client",

    )


class PortfolioORM(Base):

    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(

        Integer,

        primary_key=True,

    )

    portfolio_code: Mapped[str]

    client_id: Mapped[int] = mapped_column(

        ForeignKey("clients.id")

    )

    market_value: Mapped[float]

    client = relationship(

        "ClientORM",

        back_populates="portfolios",

    )

    holdings = relationship(

        "HoldingORM",

        back_populates="portfolio",

    )


class HoldingORM(Base):

    __tablename__ = "holdings"

    id: Mapped[int] = mapped_column(

        Integer,

        primary_key=True,

    )

    portfolio_id: Mapped[int] = mapped_column(

        ForeignKey("portfolios.id")

    )

    symbol: Mapped[str]

    asset_class: Mapped[str]

    quantity: Mapped[float]

    average_price: Mapped[float]

    current_price: Mapped[float]

    portfolio = relationship(

        "PortfolioORM",

        back_populates="holdings",

    )