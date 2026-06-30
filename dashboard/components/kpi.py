import streamlit as st


def kpis(data):

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric(
        "Portfolio",
        data["portfolio_id"],
    )

    c2.metric(
        "Value",
        f"₹{data['portfolio_value']:,.0f}",
    )

    c3.metric(
        "Drift",
        f"{data['drift']*100:.2f}%",
    )

    c4.metric(
        "Risk",
        round(data["risk_score"], 2),
    )

    c5.metric(
        "Tax",
        f"₹{data['tax_estimate']:,.0f}",
    )

    c6.metric(
        "Decision",
        data["trigger"],
    )