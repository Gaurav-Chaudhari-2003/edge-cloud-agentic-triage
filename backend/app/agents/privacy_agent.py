import re


class PrivacyAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "privacy"
        )

        state.content=(
            re.sub(
                r"\d",
                "*",
                state.content
            )
        )

        return state