def build_memory_prompt(
    memory_context: str
):

    if not memory_context:
        return None


    return {
        "role": "system",
        "content": f"""
You are a helpful AI Personal Assistant.

Use user memories only when they are relevant.

Do not invent information.
Do not assume missing details.

User Memory Context:

{memory_context}

Answer naturally.
"""
    }