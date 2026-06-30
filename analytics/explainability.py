class ExplainabilityEngine:

    def generate(self, state):

        factors = []

        score = 0

        drift_score = round(state.drift * 100 * 5)

        score += drift_score

        factors.append({

            "factor": "Portfolio Drift",

            "value": f"{state.drift*100:.2f}%",

            "impact": drift_score,

        })

        risk_score = round((state.risk_score - 1) * 100)

        score += risk_score

        factors.append({

            "factor": "Risk Score",

            "value": round(state.risk_score, 2),

            "impact": risk_score,

        })

        tax_penalty = -round(state.tax_estimate / 100)

        score += tax_penalty

        factors.append({

            "factor": "Tax Impact",

            "value": state.tax_estimate,

            "impact": tax_penalty,

        })

        compliance = 10 if state.compliance_status else -20

        score += compliance

        factors.append({

            "factor": "Compliance",

            "value": state.compliance_status,

            "impact": compliance,

        })

        approval = 15 if state.approved else -15

        score += approval

        factors.append({

            "factor": "Approval",

            "value": state.approved,

            "impact": approval,

        })

        return {

            "total_score": score,

            "factors": factors,

        }