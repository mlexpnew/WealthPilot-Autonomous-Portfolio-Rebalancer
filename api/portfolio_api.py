print("========== Portfolio API Loaded ==========")
print("Portfolio API Loaded")
from pathlib import Path
import json

from fastapi import APIRouter

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


DATA_FILE = Path("data/clients.json")


def load_clients():

    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


@router.get("/all")
def all_portfolios():

    return load_clients()


@router.get("/{portfolio_id}")
def portfolio(portfolio_id: str):

    for client in load_clients():

        if client["portfolio_id"] == portfolio_id:
            return client

    return {"error": "Portfolio not found"}


@router.get("/risk/{risk}")
def risk_category(risk: str):

    return [

        client

        for client in load_clients()

        if client["risk_category"].lower()
        == risk.lower()

    ]