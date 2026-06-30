from agents.approval_agent import ApprovalAgent
from agents.audit_agent import AuditAgent
from agents.compliance_agent import ComplianceAgent
from agents.explanation_agent import ExplanationAgent
from agents.market_agent import MarketAgent
from agents.portfolio_monitor import PortfolioMonitorAgent
from agents.risk_agent import RiskAgent
from agents.tax_agent import TaxAgent
from agents.trade_agent import TradeAgent
from agents.trigger_agent import TriggerAgent
from agents.decision_agent import DecisionAgent
from agents.hitl_agent import HumanOverrideAgent
from agents.confidence_agent import ConfidenceAgent
from monitoring.timeline import ExecutionTimeline
from monitoring.agent_metrics import AgentMetrics

class Orchestrator:

    def __init__(self):
        
        self.hitl = HumanOverrideAgent()

        self.monitor = PortfolioMonitorAgent()

        self.trigger = TriggerAgent()

        self.market = MarketAgent()

        self.risk = RiskAgent()

        self.trade = TradeAgent()

        self.tax = TaxAgent()

        self.compliance = ComplianceAgent()

        self.explainer = ExplanationAgent()

        self.approval = ApprovalAgent()

        self.audit = AuditAgent()
        
        self.decision = DecisionAgent()
        
        self.confidence = ConfidenceAgent()
        
        self.timeline = ExecutionTimeline()
        
        self.metrics = AgentMetrics()

    def run(self, state):

        state.execution_timeline = self.timeline.start()

        state = self.monitor.execute(state)
        self.metrics.record("Portfolio Monitor")
        self.timeline.log(
            state.execution_timeline,
            "Portfolio Monitor",
            "Portfolio monitoring completed",
        )

        state = self.trigger.execute(state)
        self.metrics.record("Trigger Agent")
        self.timeline.log(
            state.execution_timeline,
            "Trigger Agent",
            "Trigger evaluation completed",
        )

        state = self.hitl.execute(state)
        self.metrics.record("Human Override")
        self.timeline.log(
            state.execution_timeline,
            "Human Override",
            "Override check completed",
        )

        state = self.risk.execute(state)
        self.metrics.record("Risk Agent")
        self.timeline.log(
            state.execution_timeline,
            "Risk Agent",
            "Risk analysis completed",
        )

        state = self.market.execute(state)
        self.metrics.record("Market Agent")
        self.timeline.log(
            state.execution_timeline,
            "Market Agent",
            "Live market data collected",
        )

        state = self.decision.execute(state)
        self.metrics.record("Decision Agent")
        self.timeline.log(
            state.execution_timeline,
            "Decision Agent",
            "Decision generated",
        )

        if state.trigger == "REBALANCE":

            state = self.trade.execute(state)
            self.metrics.record("Trade Agent")
            self.timeline.log(
                state.execution_timeline,
                "Trade Agent",
                "Trade list generated",
            )

            state = self.tax.execute(state)
            self.metrics.record("Tax Agent")
            self.timeline.log(
                state.execution_timeline,
                "Tax Agent",
                "Tax estimation completed",
            )

            state = self.compliance.execute(state)
            self.metrics.record("Compliance Agent")
            self.timeline.log(
                state.execution_timeline,
                "Compliance Agent",
                "Compliance validation completed",
            )

            state = self.explainer.execute(state)
            self.metrics.record("Explanation Agent")
            self.timeline.log(
                state.execution_timeline,
                "Explanation Agent",
                "Explanation generated",
            )

            state = self.approval.execute(state)
            self.metrics.record("Approval Agent")
            self.timeline.log(
                state.execution_timeline,
                "Approval Agent",
                "Approval completed",
            )

            state = self.audit.execute(state)
            self.metrics.record("Audit Agent")
            self.timeline.log(
                state.execution_timeline,
                "Audit Agent",
                "Audit log saved",
            )

            state = self.decision.execute(state)
            self.metrics.record("Decision Agent")
            self.timeline.log(
                state.execution_timeline,
                "Decision Agent",
                "Decision updated",
            )

            state = self.confidence.execute(state)
            self.metrics.record("Confidence Agent")
            self.timeline.log(
                state.execution_timeline,
                "Confidence Agent",
                "Confidence score calculated",
            )

        state.execution_timeline = self.timeline.finish(
            state.execution_timeline
        )

        return state