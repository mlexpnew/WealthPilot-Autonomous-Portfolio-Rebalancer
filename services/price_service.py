import yfinance as yf
from utils.logger import logger

class PriceService:

    @staticmethod
    def latest_price(symbol: str):
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="2d")

            if history.empty:
                logger.warning(f"No data found for {symbol}")
                return None

            return round(float(history["Close"].iloc[-1]), 2)

        except Exception as e:
            logger.exception(f"Error fetching {symbol}: {e}")
            return None

    @staticmethod
    def get_prices(symbols):
        prices = {}

        for symbol in symbols:
            prices[symbol] = PriceService.latest_price(symbol)

        return prices