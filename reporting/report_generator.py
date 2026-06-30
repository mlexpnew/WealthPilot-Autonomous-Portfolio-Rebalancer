from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


class PortfolioReport:

    def generate(self, state):

        filename = f"reports/{state.portfolio_id}.pdf"

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>WealthPilot AI Portfolio Report</b>",
                styles["Title"],
            )
        )

        story.append(
            Paragraph(
                f"Portfolio : {state.portfolio_id}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Client : {state.client_name}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Risk Category : {state.risk_category}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Portfolio Value : ₹{state.portfolio_value:,.0f}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Drift : {state.drift*100:.2f}%",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Risk Score : {state.risk_score:.2f}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Decision : {state.trigger}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Decision Score : {state.decision_score}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Tax Estimate : ₹{state.tax_estimate:,.0f}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                "<b>Recommended Trades</b>",
                styles["Heading2"],
            )
        )

        for trade in state.trade_list:

            story.append(

                Paragraph(

                    f"{trade.action} {trade.symbol} "
                    f"{trade.quantity} @ ₹{trade.price}",

                    styles["Normal"],

                )

            )

        doc.build(story)

        return filename