import requests
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import json

st.set_page_config(
    page_title="WealthPilot AI Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 WealthPilot AI")
st.subheader("Autonomous Multi-Agent Portfolio Rebalancing System")




# =====================================
# Sidebar
# =====================================

st.sidebar.title("Portfolio Explorer")

portfolio_search = st.sidebar.text_input(
    "Portfolio ID",
    ""
)

client_search = st.sidebar.text_input(
    "Client Name",
    ""
)

risk_filter = st.sidebar.selectbox(
    "Risk Category",
    [
        "All",
        "Conservative",
        "Moderately Conservative",
        "Moderate",
        "Moderately Aggressive",
        "Aggressive",
    ],
)

with open("data/clients.json", "r") as f:
    clients = json.load(f)

client_df = pd.DataFrame(clients)

filtered = client_df.copy()

if portfolio_search:

    filtered = filtered[
        filtered["portfolio_id"]
        .str.contains(
            portfolio_search,
            case=False,
        )
    ]

if client_search:

    filtered = filtered[
        filtered["client_name"]
        .str.contains(
            client_search,
            case=False,
        )
    ]
    
st.sidebar.success(
    f"{len(filtered)} Portfolios Found"
)

# =====================================
# Load Client Dataset
# =====================================


# =====================================
# Portfolio Selector
# =====================================



with open("data/clients.json", "r") as f:
    clients = json.load(f)

client_df = pd.DataFrame(clients)



API = "http://127.0.0.1:8000"
try:

    clients = requests.get(
        f"{API}/portfolio/all"
    ).json()

    portfolio_map = {
    f"{client['client_name']} ({client['portfolio_id']})": client["portfolio_id"]
    for client in clients
}

    selected_name = st.sidebar.selectbox(
    "📁 Select Portfolio",
    list(portfolio_map.keys()),
)

    selected_portfolio = portfolio_map[selected_name]

    response = requests.get(
        f"{API}/run/{selected_portfolio}"
    )

    response.raise_for_status()

    data = response.json()

except Exception as e:

    st.error(f"Cannot connect to FastAPI.\n\n{e}")

    st.stop()


def portfolio_health(data):

    score = 100

    score -= int(data["drift"] * 100 * 2)

    score -= int((data["risk_score"] - 1) * 20)

    if not data["approved"]:
        score -= 15

    if not data["compliance_status"]:
        score -= 20

    return max(0, min(score, 100))



# ==========================
# AI Portfolio Alerts
# ==========================

st.subheader("🚨 AI Portfolio Alerts")

alerts = []

if data["drift"] >= 0.05:
    alerts.append(
        (
            "warning",
            f"Portfolio drift has reached {data['drift']*100:.2f}%. Rebalancing is recommended."
        )
    )

if data["risk_score"] > 1.0:
    alerts.append(
        (
            "error",
            f"Risk score ({data['risk_score']:.2f}) exceeds the preferred threshold."
        )
    )

if data["tax_estimate"] > 500:
    alerts.append(
        (
            "info",
            f"Estimated tax impact: ₹{data['tax_estimate']:,.0f}."
        )
    )

if data["approved"]:
    alerts.append(
        (
            "success",
            "Portfolio has passed compliance and approval checks."
        )
    )

for level, message in alerts:

    if level == "success":
        st.success(message)

    elif level == "warning":
        st.warning(message)

    elif level == "error":
        st.error(message)

    else:
        st.info(message)

st.divider()

st.subheader("Client Portfolio Database")

st.dataframe(
    filtered[
        [
            "portfolio_id",
            "client_name",
            "risk_category",
            "portfolio_value",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

selected = st.selectbox(
    "Select Portfolio",
    filtered["portfolio_id"].tolist()
)
# ==========================
# KPI CARDS
# ==========================

health = portfolio_health(data)

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

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
    f"{data['drift']*100:.2f}%"
)

c4.metric(
    "Risk Score",
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

c7.metric(
    "Health Score",
    health
)
c7.metric(
    "Confidence",
    f"{data['confidence_score']}%"
)
if health >= 85:
    status = "🟢 Excellent"
elif health >= 70:
    status = "🟡 Good"
elif health >= 50:
    status = "🟠 Warning"
else:
    status = "🔴 Critical"

c7.metric(
    "Health",
    f"{health}/100",
)

st.caption(f"Portfolio Status : {status}")

st.divider()


st.subheader("📄 AI Portfolio Report")

report_url = (
    f"{API}/report/{data['portfolio_id']}"
)

st.link_button(
    "📥 Download PDF Report",
    report_url,
)



st.subheader("📧 Email Report")

email = st.text_input(
    "Recipient Email"
)

if st.button("Send Report"):

    response = requests.post(

        f"{API}/email/{data['portfolio_id']}",

        params={
            "recipient": email,
        },

    )

    if response.status_code == 200:

        st.success(
            "Report emailed successfully."
        )

    else:

        st.error(
            response.text
        )

# ==========================
# Allocation Charts
# ==========================



st.subheader("📊 Current vs Target Allocation")

allocation = pd.DataFrame({
    "Asset": list(data["current_allocation"].keys()),
    "Current": list(data["current_allocation"].values()),
    "Target": list(data["target_allocation"].values()),
})

chart = allocation.melt(
    id_vars="Asset",
    value_vars=["Current", "Target"],
    var_name="Allocation",
    value_name="Weight",
)

fig = px.bar(
    chart,
    x="Asset",
    y="Weight",
    color="Allocation",
    barmode="group",
    text="Weight",
)

fig.update_traces(
    texttemplate="%{text:.0%}",
    textposition="outside",
)

fig.update_layout(
    yaxis_tickformat=".0%",
    height=450,
    legend_title="",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()


# ==========================
# Portfolio Drift Analysis
# ==========================

st.subheader("📉 Portfolio Drift Analysis")

drift_df = pd.DataFrame({
    "Asset": list(data["current_allocation"].keys()),
    "Current": list(data["current_allocation"].values()),
    "Target": list(data["target_allocation"].values()),
})

drift_df["Difference"] = (
    drift_df["Current"] - drift_df["Target"]
)

def status(diff):

    if diff > 0.02:
        return "🔴 Overweight"

    if diff < -0.02:
        return "🟡 Underweight"

    return "🟢 Balanced"

drift_df["Status"] = drift_df["Difference"].apply(status)

drift_df["Current"] = drift_df["Current"].map(
    lambda x: f"{x:.0%}"
)

drift_df["Target"] = drift_df["Target"].map(
    lambda x: f"{x:.0%}"
)

drift_df["Difference"] = drift_df["Difference"].map(
    lambda x: f"{x:+.0%}"
)

st.dataframe(
    drift_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()


# ==========================
# Diversification Analysis
# ==========================

st.subheader("🌍 Portfolio Diversification")

allocation = data["current_allocation"]

largest = max(allocation.values())

if largest <= 0.40:
    diversification = "Excellent"
    color = "success"

elif largest <= 0.60:
    diversification = "Good"
    color = "info"

elif largest <= 0.75:
    diversification = "Moderate"
    color = "warning"

else:
    diversification = "Poor"
    color = "error"

text = f"""
### Diversification Score

**Status:** {diversification}

Largest Allocation : **{largest:.0%}**

Number of Asset Classes : **{len(allocation)}**

Current Portfolio is distributed across:

- Equity
- Debt
- Gold
"""

if color == "success":
    st.success(text)

elif color == "info":
    st.info(text)

elif color == "warning":
    st.warning(text)

else:
    st.error(text)
    
    
    
score = int((1 - largest) * 100)

st.progress(score / 100)

st.caption(
    f"Diversification Score : {score}/100"
)


# ==========================
# AI Executive Summary
# ==========================

st.subheader("🧠 AI Executive Summary")

if data["trigger"] == "REBALANCE":

    st.warning(
        f"""
### 📌 Recommendation

The AI recommends **rebalancing** this portfolio.

• Portfolio Drift : **{data['drift']*100:.2f}%**

• Risk Score : **{data['risk_score']:.2f}**

• Estimated Tax : **₹{data['tax_estimate']:,.0f}**

• Decision Score : **{data['decision_score']}/100**

• Recommended Trades : **{len(data['trade_list'])}**

"""
    )

else:

    st.success(
        """
### ✅ Recommendation

Portfolio is aligned with its target allocation.

No action is required at this time.
"""
    )

st.divider()

st.subheader("📋 Trade Summary")

if len(data["trade_list"]) == 0:

    st.success("No trades required.")

else:

    summary = pd.DataFrame(data["trade_list"])[
        [
            "symbol",
            "action",
            "amount",
            "reason",
        ]
    ]

    summary.rename(
        columns={
            "symbol": "ETF",
            "action": "Action",
            "amount": "Amount (₹)",
            "reason": "Reason",
        },
        inplace=True,
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
    )

st.divider()


# ==========================
# Portfolio Performance
# ==========================

st.subheader("📈 Portfolio Performance")

history = pd.DataFrame({

    "Day": [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Today",
    ],

    "Portfolio Value": [
        955000,
        968000,
        978000,
        991000,
        1003000,
        data["portfolio_value"],
    ]

})

fig = px.line(

    history,

    x="Day",

    y="Portfolio Value",

    markers=True,

)

fig.update_traces(

    line_width=4,

    marker_size=10,

)

fig.update_layout(

    height=420,

    yaxis_title="Portfolio Value (₹)",

    xaxis_title="",

)

st.plotly_chart(

    fig,

    use_container_width=True,

)

st.divider()

# Live Market Overview
# ==========================

st.subheader("📈 Live Market Overview")

market = data["market_data"]

from datetime import datetime

now = datetime.now().time()

market_status = (
    "🟢 Market Open"
    if now.hour >= 9
    and (
        now.hour < 15
        or (now.hour == 15 and now.minute <= 30)
    )
    else "🔴 Market Closed"
)

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "NIFTY 50",
    f"{market['nifty']:,.2f}",
)

m2.metric(
    "BANK NIFTY",
    f"{market['bank_nifty']:,.2f}",
)

m3.metric(
    "Status",
    market_status,
)

m4.metric(
    "Updated",
    market["timestamp"][11:19],
)

st.divider()



# ==========================
# What-If Simulator
# ==========================

st.subheader("🧮 Portfolio What-If Simulator")

left, right = st.columns(2)

with left:

    equity = st.slider(
        "Equity %",
        0,
        100,
        int(data["current_allocation"]["Equity"] * 100),
    )

    debt = st.slider(
        "Debt %",
        0,
        100,
        int(data["current_allocation"]["Debt"] * 100),
    )

    gold = st.slider(
        "Gold %",
        0,
        100,
        int(data["current_allocation"]["Gold"] * 100),
    )

total = equity + debt + gold

with right:

    if total != 100:

        st.error(
            f"Allocation must total 100%. Current = {total}%"
        )

    else:

        target = data["target_allocation"]

        drift = (

            abs(equity / 100 - target["Equity"])
            + abs(debt / 100 - target["Debt"])
            + abs(gold / 100 - target["Gold"])

        ) / 2

        st.metric(
            "Estimated Drift",
            f"{drift*100:.2f}%"
        )

        if drift >= 0.05:

            st.warning(
                "AI would recommend rebalancing."
            )

        else:

            st.success(
                "Portfolio is well balanced."
            )

        st.metric(
            "Estimated Risk",
            round(
                equity / 100 * 1.5 +
                debt / 100 * 0.6 +
                gold / 100 * 0.8,
                2,
            ),
        )

st.divider()


# ==========================
# Recommended Trades
# ==========================

st.subheader("💼 Recommended Trades")

trade_df = pd.DataFrame(data["trade_list"])

if trade_df.empty:

    st.success("No trades required.")

else:

    st.dataframe(
        trade_df,
        use_container_width=True,
        hide_index=True,
    )
    

st.divider()

# ==========================
# AI Decision
# ==========================

st.subheader("🧠 AI Decision Intelligence")

left, right = st.columns([1, 2])

with left:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["decision_score"],
            title={"text": "Decision Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"thickness": 0.35},
                "steps": [
                    {"range": [0, 40], "color": "#ff4b4b"},
                    {"range": [40, 70], "color": "#ffb347"},
                    {"range": [70, 100], "color": "#4caf50"},
                ],
            },
        )
    )

    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

with right:

    st.markdown("### Decision Reasons")

    for reason in data["decision_reasons"]:

        st.success(reason)

    st.info(
        f"""
**Current Trigger:** {data["trigger"]}

**Portfolio Drift:** {data["drift"]*100:.2f}%

**Risk Score:** {data["risk_score"]:.2f}

**Estimated Tax:** ₹{data["tax_estimate"]:,.0f}
"""
    )

st.divider()



# ==========================
# Agent Pipeline
# ==========================

st.subheader("🤖 Multi-Agent Execution Pipeline")

pipeline = pd.DataFrame([
    ["Portfolio Monitor", "✅ Completed", "18 ms"],
    ["Trigger Agent", "✅ Completed", "7 ms"],
    ["Market Agent", "✅ Completed", "320 ms"],
    ["Risk Agent", "✅ Completed", "45 ms"],
    ["Decision Agent", "✅ Completed", "10 ms"],
    ["Trade Agent", "✅ Completed", "420 ms"],
    ["Tax Agent", "✅ Completed", "25 ms"],
    ["Compliance Agent", "✅ Completed", "15 ms"],
    ["Approval Agent", "✅ Completed", "8 ms"],
    ["Audit Agent", "✅ Completed", "6 ms"],
], columns=[
    "Agent",
    "Status",
    "Execution Time"
])

st.dataframe(
    pipeline,
    use_container_width=True,
    hide_index=True,
)

# ==========================
# Client Explanation
# ==========================

st.subheader("📄 Client Explanation")

st.info(
    data["explanation"]["client"]
)

st.divider()

# ==========================
# Advisor View
# ==========================

st.subheader("📊 Advisor Summary")

advisor = data["explanation"]["advisor"]

c1, c2, c3 = st.columns(3)

c1.metric(
    "Risk Score",
    advisor["risk_score"],
)

c2.metric(
    "Portfolio Drift",
    f"{advisor['portfolio_drift']*100:.2f}%"
)

c3.metric(
    "Estimated Tax",
    f"₹{advisor['tax']:,.0f}"
)

c4, c5 = st.columns(2)

c4.metric(
    "Trades",
    advisor["number_of_trades"],
)

c5.metric(
    "Trigger",
    advisor["trigger"],
)

# ==========================
# Compliance
# ==========================

st.subheader("✅ Compliance")

comp = data["explanation"]["compliance"]

if comp["approved"]:
    st.success("Compliance Status : PASSED")
else:
    st.error("Compliance Status : FAILED")

col1, col2 = st.columns(2)

col1.write(f"**Decision ID:** {comp['decision_id']}")
col1.write(f"**Trade Count:** {comp['trade_count']}")

col2.write(f"**Timestamp:** {comp['timestamp']}")
col2.write(f"**Risk Score:** {comp['risk_score']}")

# ==========================
# Approval
# ==========================

st.subheader("🟢 Approval")

approval = data["explanation"]["approval"]

if approval["status"] == "APPROVED":
    st.success("APPROVED")
else:
    st.error("REJECTED")

c1, c2 = st.columns(2)

c1.write(f"**Approval ID:** {approval['approval_id']}")
c1.write(f"**Portfolio:** {approval['portfolio_id']}")

c2.write(f"**Decision Score:** {approval['decision_score']}")
c2.write(f"**Requested At:** {approval['requested_at']}")

# ==========================
# Audit History
# ==========================

# ==========================
# Audit History
# ==========================

try:

    audit = requests.get(
        f"{API}/audit"
    ).json()

    st.subheader("📜 Audit History")

    if isinstance(audit, dict):

        history = audit.get("history", [])

    else:

        history = audit

    if len(history) == 0:

        st.warning("No audit records found.")

    else:

        audit_df = pd.DataFrame(history)

        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### 📈 AI Decision Timeline")

        timeline = audit_df.copy()

        timeline["timestamp"] = pd.to_datetime(
            timeline["timestamp"]
        )

        timeline = timeline.sort_values(
            "timestamp"
        )

        fig = px.line(
            timeline,
            x="timestamp",
            y="decision_score",
            markers=True,
            title="Decision Score History",
        )

        fig.update_traces(
            line_width=3,
            marker_size=8,
        )

        fig.update_layout(
            xaxis_title="Timestamp",
            yaxis_title="Decision Score",
            template="plotly_dark",
            height=420,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

except Exception as e:

    st.warning(
        f"Audit API unavailable: {e}"
    )

st.divider()

analytics = requests.get(
    f"{API}/analytics"
).json()

st.subheader("📊 Portfolio Analytics")

a1, a2, a3 = st.columns(3)

a1.metric(
    "Total Decisions",
    analytics.get("total_decisions", 0),
)

a2.metric(
    "Approval Rate",
    f"{analytics.get('approval_rate', 0)}%",
)

a3.metric(
    "Approved",
    analytics.get("approved", 0),
)

# second row of metrics
b1, b2, b3 = st.columns(3)

b1.metric(
    "Avg Drift",
    f"{analytics.get('average_drift', 0) * 100:.2f}%"
)

b2.metric(
    "Avg Risk",
    analytics.get("average_risk_score", 0),
)

b3.metric(
    "Avg Tax",
    f"₹{analytics.get('average_tax', 0):,.0f}"
)

st.divider()


# ==========================
# Backtest
# ==========================

# ==========================
# Backtest
# ==========================

try:

    backtest = requests.get(
        f"{API}/backtest"
    ).json()

    st.subheader("📈 Backtest Results")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Annual Return",
        f"{backtest['metrics']['annual_return']:.2f}%"
    )

    m2.metric(
        "Volatility",
        f"{backtest['metrics']['volatility']:.2f}%"
    )

    m3.metric(
        "Sharpe Ratio",
        round(backtest["metrics"]["sharpe"], 2)
    )

    m4.metric(
        "Max Drawdown",
        f"{backtest['metrics']['max_drawdown']:.2f}%"
    )

    st.divider()

    st.subheader("⚖️ AI vs Legacy Strategy")

    comparison = backtest["comparison"]

    c1, c2 = st.columns(2)

    c1.metric(
        "Tax Saved",
        f"₹{comparison['tax_saved']:,}"
    )

    c2.metric(
        "Execution Time",
        f"{comparison['execution_speed_ms']:.2f} ms"
    )

    st.success(
        f"✅ {comparison['rebalance_improvement']}"
    )

    st.info(
        f"🧠 {comparison['decision_quality']}"
    )

except Exception as e:

    st.warning(
        f"Backtest API unavailable: {e}"
    )


st.divider()

st.subheader("⚖️ Portfolio Comparison")

clients = requests.get(
    f"{API}/portfolio/all"
).json()

portfolio_ids = [
    c["portfolio_id"]
    for c in clients
]

col1, col2 = st.columns(2)

with col1:
    portfolio1 = st.selectbox(
        "Portfolio 1",
        portfolio_ids,
        key="compare1",
    )

with col2:
    portfolio2 = st.selectbox(
        "Portfolio 2",
        portfolio_ids,
        index=1,
        key="compare2",
    )

if st.button("Compare"):

    comparison = requests.get(

        f"{API}/compare",

        params={
            "portfolio1": portfolio1,
            "portfolio2": portfolio2,
        },

    ).json()

    st.json(comparison)
    

###Explainable AI.

try:

    st.divider()

    st.subheader("🧠 Explainable AI")

    explain = requests.get(
        f"{API}/explain/{data['portfolio_id']}"
    ).json()

    if "error" in explain:

        st.error(explain["error"])

    else:

        st.metric(
            "AI Score",
            explain["total_score"],
        )

        df = pd.DataFrame(
            explain["factors"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

except Exception as e:

    st.error(e)
    
    
   ####AI Recommendations" 
st.divider()

st.subheader("💡 AI Recommendations")

recommendations = requests.get(
    f"{API}/recommend/{data['portfolio_id']}"
).json()

if isinstance(recommendations, list):

    for rec in recommendations:

        if rec["priority"] == "High":

            st.error(
                f"🔴 {rec['title']}\n\n{rec['description']}"
            )

        elif rec["priority"] == "Medium":

            st.warning(
                f"🟡 {rec['title']}\n\n{rec['description']}"
            )

        else:

            st.success(
                f"🟢 {rec['title']}\n\n{rec['description']}"
            )

else:

    st.error(recommendations["error"])
    
    
####Monte Carlo Simulation
    
st.divider()

st.subheader("📈 Monte Carlo Simulation")

simulation = requests.get(

    f"{API}/simulation/{data['portfolio_id']}"

).json()

if "error" not in simulation:

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Expected",

        f"₹{simulation['expected']:,.0f}"

    )

    c2.metric(

        "Median",

        f"₹{simulation['median']:,.0f}"

    )

    c3.metric(

        "Best",

        f"₹{simulation['best']:,.0f}"

    )

    c4.metric(

        "Worst",

        f"₹{simulation['worst']:,.0f}"

    )

    df = pd.DataFrame({

        "Portfolio Value":

        simulation["distribution"]

    })

    fig = px.histogram(

        df,

        x="Portfolio Value",

        nbins=30,

        title="Monte Carlo Distribution",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

else:

    st.error(

        simulation["error"]

    )
st.divider()
####Executive Report section.

st.subheader("📄 Executive Report")

report_url = f"{API}/report/{data['portfolio_id']}"

st.link_button(

    "⬇ Download Portfolio Report",

    report_url,

)
    
st.divider()

st.subheader("🚨 Portfolio Alerts")

alerts = requests.get(
    f"{API}/alerts/{data['portfolio_id']}"
).json()

if isinstance(alerts, list):

    if len(alerts) == 0:

        st.success("No active alerts.")

    else:

        for alert in alerts:

            if alert["severity"] == "High":

                st.error(
                    f"🔴 {alert['title']}\n\n"
                    f"{alert['message']}\n\n"
                    f"{alert['time']}"
                )

            elif alert["severity"] == "Medium":

                st.warning(
                    f"🟡 {alert['title']}\n\n"
                    f"{alert['message']}\n\n"
                    f"{alert['time']}"
                )

            else:

                st.info(
                    f"🔵 {alert['title']}\n\n"
                    f"{alert['message']}\n\n"
                    f"{alert['time']}"
                )

else:

    st.error(alerts["error"]) 
    # ==========================
# Portfolio Risk Breakdown
# ==========================

st.subheader("🛡️ Portfolio Risk Breakdown")

risk = pd.DataFrame({

    "Category":[
        "Market Risk",
        "Concentration",
        "Liquidity",
        "Volatility",
        "Diversification"
    ],

    "Score":[
        70,
        65,
        90,
        58,
        82
    ]

})

fig = px.line_polar(

    risk,

    r="Score",

    theta="Category",

    line_close=True,

)

fig.update_traces(fill="toself")

fig.update_layout(
    height=500,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()



# ==========================
# Backtest
# ==========================

try:

    backtest = requests.get(
        f"{API}/backtest"
    ).json()

    ...

except Exception as e:

    st.warning(
        f"Backtest API unavailable: {e}"
    )
st.divider()

st.subheader("💬 WealthPilot AI Assistant")

question = st.text_input(
    "Ask about this portfolio"
)

if question:

    response = requests.get(

        f"{API}/chat/{data['portfolio_id']}",

        params={
            "question": question,
        },
    )

    if response.status_code == 200:

        answer = response.json()["answer"]

        st.chat_message("assistant").write(answer)

    else:

        st.error(
            "Unable to get AI response."
        )
        
#Agent Performance

      
st.divider()

st.subheader("🤖 Agent Performance")

metrics = requests.get(
    f"{API}/agent-metrics"
).json()

metrics_df = pd.DataFrame(metrics)

st.dataframe(
    metrics_df,
    use_container_width=True,
    hide_index=True,
)