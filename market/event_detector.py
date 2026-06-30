class EventDetector:

    def detect(
        self,
        market,
    ):

        nifty = market.get("nifty")

        if nifty is None:

            return False

        if market.get("volatility", 0) > 0.25:

            return True

        return False