import yfinance as yf


class PriceService:

    @staticmethod
    def latest_price(symbol: str):
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="2d")

            if history.empty:
                print(f"Warning: No data found for {symbol}")
                return None

            return round(float(history["Close"].iloc[-1]), 2)

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None

    @staticmethod
    def get_prices(symbols):
        prices = {}

        for symbol in symbols:
            prices[symbol] = PriceService.latest_price(symbol)

        return prices