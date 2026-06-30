import plotly.graph_objects as go
import streamlit as st


def decision_gauge(score):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            title={"text": "AI Decision Score"},

            gauge={

                "axis": {

                    "range": [0, 100]

                },

                "bar": {

                    "thickness": 0.45

                },

                "steps": [

                    {

                        "range": [0, 40],

                        "color": "#ff4b4b"

                    },

                    {

                        "range": [40, 70],

                        "color": "#ffb347"

                    },

                    {

                        "range": [70, 100],

                        "color": "#00cc66"

                    },

                ],

            },

        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )