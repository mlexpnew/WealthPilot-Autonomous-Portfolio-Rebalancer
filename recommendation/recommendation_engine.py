class RecommendationEngine:

    def generate(self, state):

        recommendations = []

        if state.drift > 0.05:

            recommendations.append({
                "priority": "High",
                "title": "Rebalance Portfolio",
                "description": "Portfolio drift exceeds acceptable threshold.",
            })

        if state.risk_score > 1.0:

            recommendations.append({
                "priority": "High",
                "title": "Reduce Risk",
                "description": "Consider increasing Debt allocation.",
            })

        if state.tax_estimate > 500:

            recommendations.append({
                "priority": "Medium",
                "title": "Tax Optimization",
                "description": "Execute trades in a tax-efficient manner.",
            })

        if len(state.trade_list) == 0:

            recommendations.append({
                "priority": "Low",
                "title": "Healthy Portfolio",
                "description": "No action required.",
            })

        return recommendations