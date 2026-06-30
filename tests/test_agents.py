from agents.orchestrator import Orchestrator
from core.state import PortfolioState


def test_orchestrator():

    orchestrator = Orchestrator()

    state = PortfolioState(

        portfolio_id="TEST",

        client_name="Demo",

        risk_category="Moderate",

        portfolio_value=100000,

        current_allocation={

            "Equity":0.7,

            "Debt":0.2,

            "Gold":0.1

        },

        target_allocation={

            "Equity":0.6,

            "Debt":0.3,

            "Gold":0.1

        }

    )

    result = orchestrator.run(state)

    assert result is not None