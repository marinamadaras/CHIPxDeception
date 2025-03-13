from app import llm


def generate(context, message):
    prompt=f"""
    You act the role of a medical chat bot, that is able to link facts about the patient and about medical science in order to give advice. You do not need to do this linking yourself as this will be given to you if available. I will give you a context, and a message typed by the user that is talking to you, both prefaced by a corresponding header, and you will attempt to generate an appropriate response to the user. Your replies should be succinct, to the point, and not stray too far from the context.

    Context:
    {context}

    Message:
    {message}
    """

    response = llm.client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])

    print("Output: ", response.text)

    return response.text
