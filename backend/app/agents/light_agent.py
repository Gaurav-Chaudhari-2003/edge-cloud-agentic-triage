from app.services.llm_service import (
generate
)


class LightAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "light"
        )

        prompt=f"""

Summarize briefly:

{state.content}

"""

        out=generate(

            "tinyllama",

            prompt
        )

        state.output=out

        state.confidence=.82

        return state