class ComplexityAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "complexity"
        )

        length=len(
            state.content
        )

        if length<100:

            state.complexity=.2

        elif length<400:

            state.complexity=.5

        else:

            state.complexity=.9

        return state