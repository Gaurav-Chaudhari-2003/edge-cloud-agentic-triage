class RouterAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "router"
        )

        if (
            state.complexity
            <0.5
        ):

            state.route=(
                "light"
            )

        else:

            state.route=(
                "heavy"
            )

        return state