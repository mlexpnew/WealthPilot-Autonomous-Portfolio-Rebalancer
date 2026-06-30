import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Query
from analytics.decision_analytics import DecisionAnalytics
from agents.orchestrator import Orchestrator
from config.settings import settings
from core.state import PortfolioState
from api.portfolio_api import router as portfolio_router
from analytics.portfolio_analytics import PortfolioAnalytics
import sys
import json
from pathlib import Path
from reports.report_generator import ReportGenerator
from fastapi.responses import FileResponse
from chat.portfolio_chat import PortfolioChat
from analytics.portfolio_compare import PortfolioComparison
from analytics.explainability import ExplainabilityEngine
from recommendation.recommendation_engine import RecommendationEngine
from simulation.monte_carlo import MonteCarloSimulator
from reporting.report_generator import PortfolioReport
from alerts.alert_engine import AlertEngine

from services.email_service import EmailService
from config.email_settings import (
    SENDER_EMAIL,
    APP_PASSWORD,
)


analytics = PortfolioAnalytics()

report_generator = ReportGenerator()

chatbot = PortfolioChat()

comparison_engine = PortfolioComparison()

xai = ExplainabilityEngine()

recommendation_engine = RecommendationEngine()

simulator = MonteCarloSimulator()

report_generator = PortfolioReport()

alert_engine = AlertEngine()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

app.include_router(portfolio_router)
from utils.logger import logger

from starlette.routing import Route

logger.info("REGISTERED ROUTES")

for route in app.routes:
    if isinstance(route, Route):
        logger.info(route.path)

orchestrator = Orchestrator()
analytics = DecisionAnalytics()


email_service = EmailService(
    SENDER_EMAIL,
    APP_PASSWORD,
)


@app.get("/override")
def override(
    action: str = Query(
        default="APPROVE"
    )
):

    portfolio = PortfolioState(

        portfolio_id="WP-1001",

        client_name="Rahul Sharma",

        risk_category="Moderate",

        current_allocation={
            "Equity":0.68,
            "Debt":0.22,
            "Gold":0.10
        },

        target_allocation={
            "Equity":0.60,
            "Debt":0.30,
            "Gold":0.10
        }
    )

    result = orchestrator.run(portfolio)

    result = orchestrator.hitl.execute(
        result,
        action
    )

    return result.model_dump()


   


@app.get("/audit")
def audit_history():

    file = Path("audit_logs/audit_history.json")

    if not file.exists():

        return {
            "count": 0,
            "history": [],
        }

    try:

        with open(file, "r") as f:

            history = json.load(f)

    except Exception:

        history = []

    history.reverse()

    return {
        "count": len(history),
        "history": history,
    }
    

@app.get("/analytics")
def analytics_summary():

    return analytics.summary()




from backtesting.backtest_engine import BacktestEngine

engine = BacktestEngine()
@app.get("/backtest")
def backtest():

    portfolio = PortfolioState(

        portfolio_id="WP-1001",

        client_name="Rahul Sharma",

        risk_category="Moderate",

        current_allocation={
            "Equity": 0.68,
            "Debt": 0.22,
            "Gold": 0.10,
        },

        target_allocation={
            "Equity": 0.60,
            "Debt": 0.30,
            "Gold": 0.10,
        },
    )

    return engine.compare(portfolio)


@app.get("/")
def home():

    return {
        "application": settings.APP_NAME,
        "status": "running",
    }


@app.get("/health")
def health():

    return {"status": "healthy"}


@app.get("/test")
def test_pipeline():

    portfolio = PortfolioState(

        portfolio_id="WP-1001",

        client_name="Rahul Sharma",

        risk_category="Moderate",

        current_allocation={
            "Equity": 0.68,
            "Debt": 0.22,
            "Gold": 0.10,
        },

        target_allocation={
            "Equity": 0.60,
            "Debt": 0.30,
            "Gold": 0.10,
        },
    )
    
    result = orchestrator.run(portfolio)

    return result.model_dump()


@app.get("/run/{portfolio_id}")
def run_portfolio(portfolio_id: str):

    with open("data/clients.json") as f:
        clients = json.load(f)

    for client in clients:

        if client["portfolio_id"] == portfolio_id:

            portfolio = PortfolioState(**client)

            result = orchestrator.run(portfolio)

            return result.model_dump()

    return {
        "error": "Portfolio not found"
    }
    
    
@app.get("/report/{portfolio_id}")
def report(portfolio_id: str):

    with open("data/clients.json") as f:

        clients = json.load(f)

    for client in clients:

        if client["portfolio_id"] == portfolio_id:

            portfolio = PortfolioState(**client)

            result = orchestrator.run(portfolio)

            pdf = report_generator.generate(
                result.model_dump()
            )

            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename=Path(pdf).name,
            )

    return {
        "error": "Portfolio not found"
    }
@app.post("/email/{portfolio_id}")
def send_email(

    portfolio_id: str,

    recipient: str,

):

    with open("data/clients.json") as f:

        clients = json.load(f)

    for client in clients:

        if client["portfolio_id"] == portfolio_id:

            portfolio = PortfolioState(**client)

            result = orchestrator.run(portfolio)

            pdf = report_generator.generate(
                result.model_dump()
            )

            return email_service.send_report(

                recipient,

                pdf,

                client["client_name"],

            )

    return {

        "error": "Portfolio not found"

    }
    
    
@app.get("/chat/{portfolio_id}")
def chat(

    portfolio_id: str,

    question: str,

):

    with open("data/clients.json") as f:

        clients = json.load(f)

    for client in clients:

        if client["portfolio_id"] == portfolio_id:

            portfolio = PortfolioState(

                portfolio_id=client["portfolio_id"],
                client_name=client["client_name"],
                risk_category=client["risk_category"],
                portfolio_value=client["portfolio_value"],
                current_allocation=client["current_allocation"],
                target_allocation=client["target_allocation"],
            )

            result = orchestrator.run(portfolio)

            return {

                "question": question,

                "answer": chatbot.reply(

                    question,

                    result.model_dump(),

                ),

            }

    return {

        "error": "Portfolio not found"

    }
    
    
@app.get("/compare")
def compare(

    portfolio1: str,

    portfolio2: str,

):

    with open("data/clients.json") as f:

        clients = json.load(f)

    result1 = None

    result2 = None

    for client in clients:

        if client["portfolio_id"] == portfolio1:

            state = PortfolioState(

                portfolio_id=client["portfolio_id"],

                client_name=client["client_name"],

                risk_category=client["risk_category"],

                portfolio_value=client["portfolio_value"],

                current_allocation=client["current_allocation"],

                target_allocation=client["target_allocation"],

            )

            result1 = orchestrator.run(
                state
            ).model_dump()

        if client["portfolio_id"] == portfolio2:

            state = PortfolioState(

                portfolio_id=client["portfolio_id"],

                client_name=client["client_name"],

                risk_category=client["risk_category"],

                portfolio_value=client["portfolio_value"],

                current_allocation=client["current_allocation"],

                target_allocation=client["target_allocation"],

            )

            result2 = orchestrator.run(
                state
            ).model_dump()

    if result1 is None or result2 is None:

        return {

            "error":

            "Portfolio not found"

        }

    return comparison_engine.compare(

        result1,

        result2,

    )

@app.get("/explain/{portfolio_id}")
def explain(portfolio_id: str):

    with open("data/clients.json") as f:

        clients = json.load(f)

    for client in clients:

        if client["portfolio_id"] == portfolio_id:

            portfolio = PortfolioState(

                portfolio_id=client["portfolio_id"],

                client_name=client["client_name"],

                risk_category=client["risk_category"],

                portfolio_value=client["portfolio_value"],

                current_allocation=client["current_allocation"],

                target_allocation=client["target_allocation"],

            )

            result = orchestrator.run(portfolio)

            return xai.generate(result)

    return {

        "error": "Portfolio not found"

    }



@app.get("/recommend/{portfolio_id}")
def recommend(portfolio_id: str):

    with open("data/clients.json") as f:

        clients = json.load(f)

    for client in clients:

        if client["portfolio_id"] == portfolio_id:

            portfolio = PortfolioState(**client)

            result = orchestrator.run(portfolio)

            return recommendation_engine.generate(result)

    return {"error": "Portfolio not found"}


@app.get("/simulation/{portfolio_id}")
def simulation(portfolio_id: str):

    with open("data/clients.json") as f:

        clients = json.load(f)

    for client in clients:

        if client["portfolio_id"] == portfolio_id:

            return simulator.simulate(

                client["portfolio_value"]

            )

    return {

        "error": "Portfolio not found"

    }
    
    
from fastapi.responses import FileResponse


@app.get("/report/{portfolio_id}")
def report(portfolio_id: str):

    with open("data/clients.json") as f:

        clients = json.load(f)

    for client in clients:

        if client["portfolio_id"] == portfolio_id:

            portfolio = PortfolioState(

                portfolio_id=client["portfolio_id"],

                client_name=client["client_name"],

                risk_category=client["risk_category"],

                portfolio_value=client["portfolio_value"],

                current_allocation=client["current_allocation"],

                target_allocation=client["target_allocation"],

            )

            result = orchestrator.run(portfolio)

            file = report_generator.generate(result)

            return FileResponse(

                file,

                media_type="application/pdf",

                filename=f"{portfolio_id}.pdf",

            )

    return {

        "error": "Portfolio not found"

    }
    
    
@app.get("/alerts/{portfolio_id}")
def alerts(portfolio_id: str):

    with open("data/clients.json") as f:
        clients = json.load(f)

    for client in clients:

        if client["portfolio_id"] == portfolio_id:

            portfolio = PortfolioState(

                portfolio_id=client["portfolio_id"],
                client_name=client["client_name"],
                risk_category=client["risk_category"],
                portfolio_value=client["portfolio_value"],
                current_allocation=client["current_allocation"],
                target_allocation=client["target_allocation"],
            )

            result = orchestrator.run(portfolio)

            return alert_engine.generate(result)

    return {
        "error": "Portfolio not found"
    }
    
@app.get("/agent-metrics")
def agent_metrics():

    return orchestrator.metrics.summary()