class ClientExplainer:

    def generate(self, state):

        if state.trigger == "REBALANCE":

            return (
                f"Your portfolio has drifted by "
                f"{state.drift:.2%}. "
                "We recommend rebalancing to restore "
                "your target allocation."
            )

        return (
            "Your portfolio is currently aligned "
            "with your target allocation."
        )