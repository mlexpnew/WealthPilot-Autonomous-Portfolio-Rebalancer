from datetime import datetime

import yfinance as yf


class MarketDataService:

    def get_price(self, ticker: str):

        stock = yf.Ticker(ticker)

        data = stock.history(period="5d")

        if data.empty:
            return None

        return round(float(data["Close"].iloc[-1]), 2)

    def get_returns(self, ticker: str, period="6mo"):

        stock = yf.Ticker(ticker)

        data = stock.history(period=period)

        if data.empty:
            return []

        returns = data["Close"].pct_change().dropna()

        return returns.tolist()

    def market_snapshot(self):

        nifty = self.get_price("^NSEI")
        banknifty = self.get_price("^NSEBANK")

        return {
            "timestamp": datetime.now().isoformat(),
            "nifty": nifty,
            "bank_nifty": banknifty,
        }