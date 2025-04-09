import app


def generate(context, question):
    out = app.llm.pipe(f"Context: {context}\n\nQuestion: {question}\n\nAnswer: ")[0]['generated_text']

    out_split = ('.' + out).split("Answer:")[-1]
    print("Output: ", out)

    return out_split