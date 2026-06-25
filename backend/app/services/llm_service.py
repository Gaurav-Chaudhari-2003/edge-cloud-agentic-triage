import ollama


def generate(
    model,
    prompt
):

    res=ollama.chat(

        model=model,

        messages=[

            {
                "role":"user",

                "content":prompt
            }

        ]

    )

    return (
        res["message"]
        ["content"]
    )