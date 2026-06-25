class InputAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "input"
        )

        state.content=(
            state.content
            .strip()
        )

        return state