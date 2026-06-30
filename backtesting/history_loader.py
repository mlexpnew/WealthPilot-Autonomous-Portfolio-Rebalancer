import yfinance as yf
import numpy as np


class HistoryLoader:

    @staticmethod
    def load_returns():

        data = yf.download(

            "^NSEI",

            period="1y",

            interval="1d",

            progress=False,

        )

        if data.empty:

            return np.random.normal(
                0.001,
                0.015,
                252,
            )

        returns = data["Close"].pct_change().dropna()

        return returns.values