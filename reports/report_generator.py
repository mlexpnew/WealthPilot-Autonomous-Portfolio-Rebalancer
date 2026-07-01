from pathlib import Path
from reportlab.lib.styles import getSampleStyleSheet  # type: ignore[import]
from reportlab.platypus import (  # type: ignore[import]
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors  # type: ignore[import]


class ReportGenerator:

    def __init__(self):

        self.output = Path("generated_reports")

        self.output.mkdir(exist_ok=True)

        self.styles = getSampleStyleSheet()

    def generate(self, data: dict):

        filename = (
            self.output
            / f"{data['portfolio_id']}_report.pdf"
        )

        doc = SimpleDocTemplate(str(filename))

        story = []

        title = Paragraph(
            "<b><font size=20>WealthPilot AI Report</font></b>",
            self.styles["Title"],
        )

        story.append(title)

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Client Information</b>",
                self.styles["Heading2"],
            )
        )

        info = Table(
            [
                ["Portfolio ID", data["portfolio_id"]],
                ["Client", data["client_name"]],
                ["Risk Category", data["risk_category"]],
                [
                    "Portfolio Value",
                    f"₹{data['portfolio_value']:,.0f}",
                ],
            ]
        )

        info.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        story.append(info)

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Current Allocation</b>",
                self.styles["Heading2"],
            )
        )

        allocation = [["Asset", "Weight"]]

        for k, v in data["current_allocation"].items():

            allocation.append(
                [k, f"{v*100:.2f}%"]
            )

        table = Table(allocation)

        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ]
            )
        )

        story.append(table)

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Recommended Trades</b>",
                self.styles["Heading2"],
            )
        )

        trade_rows = [[
            "Symbol",
            "Action",
            "Amount",
            "Qty",
        ]]

        for t in data["trade_list"]:

            trade_rows.append(
                [
                    t["symbol"],
                    t["action"],
                    f"₹{t['amount']:,.0f}",
                    t["quantity"],
                ]
            )

        trades = Table(trade_rows)

        trades.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.orange),
                ]
            )
        )

        story.append(trades)

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Risk Summary</b>",
                self.styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                f"Risk Score : {data['risk_score']}",
                self.styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Portfolio Drift : {data['drift']*100:.2f}%",
                self.styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Decision Score : {data['decision_score']}",
                self.styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"AI Confidence : {data.get('confidence_score',0)}%",
                self.styles["BodyText"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>AI Recommendation</b>",
                self.styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                data["explanation"]["client"],
                self.styles["BodyText"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Compliance</b>",
                self.styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                f"Approved : {data['approved']}",
                self.styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Tax Estimate : ₹{data['tax_estimate']:,.0f}",
                self.styles["BodyText"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Decision Reasons</b>",
                self.styles["Heading2"],
            )
        )

        for reason in data["decision_reasons"]:

            story.append(
                Paragraph(
                    f"• {reason}",
                    self.styles["BodyText"],
                )
            )

        doc.build(story)

        return str(filename)