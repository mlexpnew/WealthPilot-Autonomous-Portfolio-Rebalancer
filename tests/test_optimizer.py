from optimizer.trade_optimizer import TradeOptimizer


def test_optimizer():

    optimizer = TradeOptimizer()

    prices = {

        "NIFTYBEES.NS": 280,

        "LIQUIDBEES.NS": 1000,

        "GOLDBEES.NS": 80,

    }

    trades = optimizer.generate_trades(

        portfolio_value=100000,

        current={

            "Equity":0.7,

            "Debt":0.2,

            "Gold":0.1,

        },

        target={

            "Equity":0.6,

            "Debt":0.3,

            "Gold":0.1,

        },

        prices=prices,

    )

    assert isinstance(trades, list)