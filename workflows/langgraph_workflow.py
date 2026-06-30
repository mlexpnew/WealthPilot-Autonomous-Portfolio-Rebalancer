from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from core.state import PortfolioGraphState

from agents.portfolio_monitor import PortfolioMonitorAgent
from agents.trigger_agent import TriggerAgent
from agents.market_agent import MarketAgent
from agents.risk_agent import RiskAgent
from agents.trade_agent import TradeAgent
from agents.tax_agent import TaxAgent
from agents.compliance_agent import ComplianceAgent
from agents.explanation_agent import ExplanationAgent
from agents.approval_agent import ApprovalAgent
from agents.audit_agent import AuditAgent


monitor = PortfolioMonitorAgent()
trigger = TriggerAgent()
market = MarketAgent()
risk = RiskAgent()
trade = TradeAgent()
tax = TaxAgent()
compliance = ComplianceAgent()
explainer = ExplanationAgent()
approval = ApprovalAgent()
audit = AuditAgent()


def monitor_node(state):
    return monitor.execute(state)


def trigger_node(state):
    return trigger.execute(state)


def market_node(state):
    return market.execute(state)


def risk_node(state):
    return risk.execute(state)


def trade_node(state):
    return trade.execute(state)


def tax_node(state):
    return tax.execute(state)


def compliance_node(state):
    return compliance.execute(state)


def explanation_node(state):
    return explainer.execute(state)


def approval_node(state):
    return approval.execute(state)


def audit_node(state):
    return audit.execute(state)


builder = StateGraph(PortfolioGraphState)

builder.add_node("monitor", monitor_node)
builder.add_node("trigger", trigger_node)
builder.add_node("market", market_node)
builder.add_node("risk", risk_node)
builder.add_node("trade", trade_node)
builder.add_node("tax", tax_node)
builder.add_node("compliance", compliance_node)
builder.add_node("explanation", explanation_node)
builder.add_node("approval", approval_node)
builder.add_node("audit", audit_node)

builder.add_edge(START, "monitor")
builder.add_edge("monitor", "trigger")
builder.add_edge("trigger", "market")
builder.add_edge("market", "risk")
builder.add_edge("risk", "trade")
builder.add_edge("trade", "tax")
builder.add_edge("tax", "compliance")
builder.add_edge("compliance", "explanation")
builder.add_edge("explanation", "approval")
builder.add_edge("approval", "audit")
builder.add_edge("audit", END)

graph = builder.compile()