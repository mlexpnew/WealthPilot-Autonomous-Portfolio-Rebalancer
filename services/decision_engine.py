from dataclasses import dataclass


@dataclass
class DecisionResult:
    should_rebalance: bool
    score: float
    reasons: list[str]


class DecisionEngine:

    DRIFT_THRESHOLD = 5.0
    DECISION_THRESHOLD = 40

    def evaluate(
        self,
        *,
        drift: float,
        risk_score: float,
        volatility: float,
        calendar_due: bool,
        market_event: bool,
    ) -> DecisionResult:

        score = 0
        reasons = []

        if drift >= self.DRIFT_THRESHOLD:
            score += 40
            reasons.append(f"Portfolio drift is {drift:.2f}%.")

        if risk_score >= 1:
            score += 20
            reasons.append("Portfolio risk exceeds acceptable threshold.")

        if volatility >= 1:
            score += 20
            reasons.append("Market volatility is elevated.")

        if calendar_due:
            score += 10
            reasons.append("Calendar-based rebalance due.")

        if market_event:
            score += 10
            reasons.append("Market event detected.")

        return DecisionResult(
            should_rebalance=score >= self.DECISION_THRESHOLD,
            score=score,
            reasons=reasons,
        )