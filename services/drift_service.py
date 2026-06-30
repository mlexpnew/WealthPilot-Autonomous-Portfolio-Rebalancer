from typing import Dict


class DriftService:
    @staticmethod
    def calculate(
        current: Dict[str, float],
        target: Dict[str, float],
    ) -> dict:

        drift = {}
        turnover = 0.0

        for asset in target:
            current_weight = current.get(asset, 0.0)
            target_weight = target.get(asset, 0.0)

            difference = current_weight - target_weight

            drift[asset] = round(difference, 4)
            turnover += abs(difference)

        return {
            "asset_drift": drift,
            "turnover": round(turnover / 2, 4),
        }