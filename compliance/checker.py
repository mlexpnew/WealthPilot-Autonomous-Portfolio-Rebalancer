from compliance.rules import *


class ComplianceChecker:

    def validate(self, state):

        errors = []

        allocation = state.target_allocation

        if allocation.get("Equity", 0) > MAX_EQUITY:

            errors.append(

                "Equity allocation exceeds limit."

            )

        if allocation.get("Debt", 0) > MAX_DEBT:

            errors.append(

                "Debt allocation exceeds limit."

            )

        if allocation.get("Gold", 0) > MAX_GOLD:

            errors.append(

                "Gold allocation exceeds limit."

            )

        for trade in state.trade_list:

            if trade["amount"] > MAX_SINGLE_TRADE:

                errors.append(

                    f'{trade["symbol"]} exceeds max trade value.'

                )

        state.compliance_status = len(errors) == 0

        return errors