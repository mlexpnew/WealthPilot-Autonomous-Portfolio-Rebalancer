import pandas as pd
import streamlit as st


def trades(data):

    if len(data) == 0:

        st.success(
            "No trades required."
        )

        return

    df = pd.DataFrame(data)

    def colour(v):

        if v == "BUY":

            return "background-color:#d4f4dd"

        return "background-color:#ffd6d6"

    st.dataframe(

        df.style.map(
            colour,
            subset=["action"],
        ),

        use_container_width=True,

        hide_index=True,

    )