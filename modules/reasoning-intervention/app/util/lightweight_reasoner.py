import re
from typing import Optional, List
from typing import Dict, Any, Optional
from flask import current_app
from app.util.ai_api_connector import generate
from pydantic import BaseModel, Field
from datetime import datetime



class LightweightReasoner:
    system_prompt = """You are an NLU processing module within a chat-bot based diabetes support system. 
                    You will be given the user's textual input and you must respond with only a JSON object conforming to the provided schema. """
    
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.turn_count = 0
        self.context = {
            "intent": None,                 # e.g., "log_blood_glucose", "ask_question", etc.
            "glucose_level": None,
            "glucose_unit": None,          # "mg/dL" or "mmol/L"
            "measurement_time": None,      # ISO format: "YYYY-MM-DDTHH:MM:SS"
            "meal_context": None,          # e.g., "before_breakfast", "after_dinner"
            "symptom": None,
            "mood": None,                  # e.g., "frustrated", "okay", "happy"
            "exercise": None,              # could later be structured into type + duration
            "medication_taken": None,      # True/False
            "medication_name": None,
            "question_topic": None,        # e.g., "diet", "medication", "symptoms"
            "confidence": None,            # e.g., "low", "medium", "high"
            "reason_for_message": None,    # e.g., "routine_logging", "alert", "feeling_unwell"

            "fallback_fields": [],         # list of keys the reasoner couldn’t confidently fill
            "other": []                    # unstructured or ambiguous input
        }

        app.extensions = getattr(app, "extensions", {})
        app.extensions["reasoner"] = self
        app.logger.warn(f"44444444444 iniltizlies")

    def process_input(self, user_input: str) -> Dict[str, Any]:
        self.turn_count += 1
        text = user_input.lower()
        datey = generate(user_input)

        # self._extract_food(text)
        # self._extract_logging(text)
        # self._extract_mood(text)
        # self._extract_adherence(text)
        # Add more extractors here

        should_ask_question = self._should_continue_with_question(text)
        if(should_ask_question):
            typey = 'Q'
        else: typey = 'A'
        return {
            "data": datey,
            "type": typey
        }

    # --------------------------
    # Context Extractor Methods
    # --------------------------

    def _extract_food(self, text: str):
        food_keywords = ["donut", "salad", "pizza", "sandwich"]  # Extend as needed
        for food in food_keywords:
            if food in text:
                self.context["mentioned_food"] = food
                break

    def _extract_logging(self, text: str):
        if re.search(r"(didn[’']?t log|forgot to log|did not log)", text):
            self.context["meals_logged"] = False
        elif re.search(r"(i logged|i tracked|i entered)", text):
            self.context["meals_logged"] = True

    def _extract_mood(self, text: str):
        mood_map = {
            "stressed": "stressed",
            "guilty": "guilty",
            "tired": "tired",
            "okay": "neutral",
            "fine": "neutral",
            # Extend as needed
        }
        for mood_word, mood_value in mood_map.items():
            if mood_word in text:
                self.context["mood"] = mood_value
                break

    def _extract_adherence(self, text: str):
        if "i did okay" in text or "i stuck to it" in text:
            self.context["self_assessed_adherence"] = "positive"
        elif "i messed up" in text or "i failed" in text:
            self.context["self_assessed_adherence"] = "negative"

    # --------------------------
    # Dialogue Control Logic
    # --------------------------

    def _should_continue_with_question(self, sentence: str) -> bool:
        # Naive placeholder
        words = ["how", "why", "who", "?"]

        sentence_words = sentence.lower().split()

        found = any(word in sentence_words for word in words)
        # current_app.logger.warn(f"7777777777FOUND      {found}")
        return found
    
    # def checkUserIsAskingQuestion(sentence: str):
    # words = ["how", "why", "who", "?"]

    # sentence_words = sentence.lower().split()

    # found = any(word in sentence_words for word in words)
    # current_app.logger.warn(f"7777777777FOUND      {found}")