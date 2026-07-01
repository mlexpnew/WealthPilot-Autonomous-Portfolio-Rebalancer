import math
from typing import Dict, List
from utils.logger import logger

from models.trade import Trade, TradeAction


class TradeOptimizer:

    def __init__(self):

        self.asset_mapping = {
            "Equity": "NIFTYBEES.NS",
            "Debt": "LIQUIDBEES.NS",
            "Gold": "GOLDBEES.NS",
        }

    def generate_trades(
        self,
        portfolio_value: float,
        current: Dict[str, float],
        target: Dict[str, float],
        prices: Dict[str, float],
    ) -> List[Trade]:

        trades: List[Trade] = []

        for asset in target.keys():

            current_weight = current.get(asset, 0.0)
            target_weight = target.get(asset, 0.0)

            diff = target_weight - current_weight

            if abs(diff) < 0.001:
                continue

            ticker = self.asset_mapping.get(asset)

            if ticker is None:
                continue

            price = prices.get(ticker)

            # Skip invalid prices
            if (
                price is None
                or not isinstance(price, (int, float))
                or math.isnan(price)
                or math.isinf(price)
                or price <= 0
            ):
                logger.warning( f"[TradeOptimizer] Skipping {ticker} - Invalid price: {price}")
                continue

            amount = abs(diff) * portfolio_value

            quantity = round(amount / price, 2)

            # Skip invalid quantities
            if (
                math.isnan(quantity)
                or math.isinf(quantity)
                or quantity <= 0
            ):
                logger.warning( f"[TradeOptimizer] Skipping {ticker} - Invalid quantity: {quantity}")
                continue

            trades.append(
                Trade(
                    symbol=ticker,
                    asset_class=asset,
                    action=TradeAction.BUY if diff > 0 else TradeAction.SELL,
                    current_weight=current_weight,
                    target_weight=target_weight,
                    weight_difference=round(diff, 4),
                    amount=round(amount, 2),
                    quantity=quantity,
                    price=round(price, 2),
                    reason=f"Rebalance {asset}",
                )
            )

        return trades