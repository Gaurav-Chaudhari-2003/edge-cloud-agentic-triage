class FormatterAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "formatter"
        )

        return {

            "request_id":
            state.request_id,

            "route":
            state.route,

            "complexity":
            state.complexity,

            "confidence":
            state.confidence,

            "agent":
            state.current_agent,

            "result":
            state.output,

            "latency_ms":
            state.latency_ms,

            "used_model":
            (
                "TinyLlama"
                if state.route == "light"
                else "Qwen"
            )
        }