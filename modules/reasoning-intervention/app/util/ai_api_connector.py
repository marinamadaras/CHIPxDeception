import app
from flask import current_app
from google.genai import types
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from typing import Dict, Any, Optional

# this method makes the actual call to the LLM
def generate(prompt, system_prompt = ""):
    response = app.llm.client.models.generate_content(model="gemini-2.0-flash", 
                                                      contents=[prompt], 
                                                      config=types.GenerateContentConfig(
                                                          temperature = 0,
                                                          seed = 45362,
                                                          system_instruction=system_prompt,
                                                          responseMimeType = "application/json",
                                                          responseSchema = DiabetesContext
                                                      ))
    current_app.logger.warn("SUPPPPPPPP HOMI")
    resp = response.text
    app.logger.warn(f"RESPONSE IS!!!!!   {resp}")
    return resp

class OtherItem(BaseModel):
    raw_text: str
    possible_category: Optional[str] = None
    confidence: Optional[float] = None


class DiabetesContext(BaseModel):
    intent: Optional[str] = None
    glucose_level: Optional[float] = None
    glucose_unit: Optional[str] = None  # "mg/dL" or "mmol/L"
    measurement_time: Optional[datetime] = None
    meal_context: Optional[str] = None
    symptom: Optional[str] = None
    mood: Optional[str] = None
    exercise: Optional[str] = None
    medication_taken: Optional[bool] = None
    medication_name: Optional[str] = None
    question_topic: Optional[str] = None
    confidence: Optional[str] = None  # e.g., "low", "medium", "high"
    reason_for_message: Optional[str] = None  # e.g., "routine_logging", "alert"
    fallback_fields: List[str] = Field(default_factory=list)
    other: List[OtherItem] = Field(default_factory=list)