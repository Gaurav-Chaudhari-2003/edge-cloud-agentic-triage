from app.services.llm_service import (
generate
)


class HeavyAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "heavy"
        )

        prompt=f"""

Analyze deeply.

Input:

{state.content}

Provide:

Summary

Priority

Actions

"""

        out=generate(

            "qwen2.5:7b",

            prompt
        )

        state.output=out

        state.confidence=.93

        return state