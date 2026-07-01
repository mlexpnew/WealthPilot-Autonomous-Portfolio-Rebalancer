# WealthPilot – Autonomous Portfolio Rebalancer

## Overview

WealthPilot is a production-style multi-agent AI system that autonomously monitors investment portfolios, evaluates risk, recommends rebalancing actions, estimates tax impact, validates compliance, and generates explainable recommendations.

---

## Features

- Multi-Agent Architecture
- Portfolio Monitoring
- Risk Analysis
- Live Market Data
- Trade Optimization
- Decision Engine
- Human-in-the-Loop Approval
- Compliance Validation
- Audit Logging
- Decision Analytics
- Portfolio Analytics
- Explainable AI
- Portfolio Comparison
- Monte Carlo Simulation
- PDF Report Generation
- Alerts & Notifications
- Agent Execution Timeline
- Agent Performance Metrics
- Docker Support
- FastAPI Backend
- Streamlit Dashboard

---

## Architecture

(Add architecture diagram here)

---

## Workflow

Client Portfolio

↓

Portfolio Monitor Agent

↓

Trigger Agent

↓

Risk Agent

↓

Market Agent

↓

Decision Agent

↓

Trade Agent

↓

Tax Agent

↓

Compliance Agent

↓

Approval Agent

↓

Audit Agent

↓

Dashboard

---

## Technology Stack

- Python
- FastAPI
- Streamlit
- Pydantic
- Plotly
- Pandas
- NumPy
- yFinance
- Docker
- ReportLab

---

## Folder Structure

(Add project tree)

---

## Installation

```bash
git clone <repo>

cd WealthPilot-Autonomous-Portfolio-Rebalancer

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app:app --reload

streamlit run dashboard/app.py


## Documentation

See /docs folder.



#####Docker
docker compose build
docker compose up


API Endpoints
/
/health
/test
/portfolio/all
/portfolio/{portfolio_id}
/run/{portfolio_id}
/analytics
/audit
/backtest
/simulation/{portfolio_id}
/recommend/{portfolio_id}
/alerts/{portfolio_id}
/timeline/{portfolio_id}
/agent-metrics
/report/{portfolio_id}

##Dashboard


####Future Enhancements
OAuth Authentication
Multi-user Support
Kubernetes Deployment
Cloud Deployment
Redis Cache
PostgreSQL


License

MIT
