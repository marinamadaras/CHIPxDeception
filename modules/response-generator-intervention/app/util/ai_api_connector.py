import app
from flask import current_app
from google.genai import types

# this method makes the actual call to the LLM
def generate(prompt, system_prompt):
    response = app.llm.client.models.generate_content(model="gemini-2.0-flash", 
                                                      contents=[prompt], 
                                                      config=types.GenerateContentConfig(
                                                          temperature = 0,
                                                          seed = 45362,
                                                          system_instruction=system_prompt
                                                      ))
    return response.text
