from app import llm


def generate(context, question):
    # prompt = "Tell me about AI"
    # prompt_template=f'''Below is an instruction that describes a task. Write a response that appropriately completes the request.

    # ### Instruction:
    # {prompt}

    # ### Response:

    # '''
    # question = "What are the symptoms of diabetes?"
    # context = "Diabetes is a metabolic disease that causes high blood sugar. The symptoms include increased thirst, frequent urination, and unexplained weight loss."
    # print("\n\n*** Generate:")

    # tokens = llm.tokenizer(
    #     f"Context: {context}\n\nQuestion: {question}\n\nAnswer: ",
    #     return_tensors='pt'
    # ).input_ids.cuda()

    # # Generate output
    # generation_output = llm.model.generate(
    #     tokens,
    #     do_sample=True,
    #     temperature=0.7,
    #     top_p=0.95,
    #     top_k=40,
    #     max_new_tokens=512
    # )

    # out = llm.tokenizer.decode(generation_output[0])


    # from transformers import pipeline

    # pipe = pipeline(
    #     "text-generation",
    #     model=llm.model,
    #     tokenizer=llm.tokenizer,
    #     max_new_tokens=512,
    #     do_sample=True,
    #     temperature=0.7,
    #     top_p=0.95,
    #     top_k=40,
    #     repetition_penalty=1.1
    # )

    # out = pipe("What are the symptoms of diabetes?")[0]['generated_text']

    # from transformers import pipeline

    # pl = pipeline("text-generation", model="medalpaca/medalpaca-7b", tokenizer="medalpaca/medalpaca-7b")
    # question = "What are the symptoms of diabetes?"
    # context = "Diabetes is a metabolic disease that causes high blood sugar. The symptoms include increased thirst, frequent urination, and unexplained weight loss."
    out = llm.pipe(f"Context: {context}\n\nQuestion: {question}\n\nAnswer: ")[0]['generated_text']

    out_split = ('.' + out).split("Answer:")[-1]
    print("Output: ", out)

    return out_split

# # Inference can also be done using transformers' pipeline
# from transformers import pipeline

# print("*** Pipeline:")
# pipe = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_new_tokens=512,
#     do_sample=True,
#     temperature=0.7,
#     top_p=0.95,
#     top_k=40,
#     repetition_penalty=1.1
# )

# print(pipe(prompt_template)[0]['generated_text'])