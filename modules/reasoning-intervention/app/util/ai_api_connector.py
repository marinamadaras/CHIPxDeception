import app
from flask import current_app
from google.genai import types
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from typing import Dict, Any, Optional, Literal

def process_input(prompt, system_prompt = ""):
    response = app.llm.client.models.generate_content(model="gemini-2.0-flash", 
                                                      contents=[prompt], 
                                                      config=types.GenerateContentConfig(
                                                          temperature = 0,
                                                          seed = 45362,
                                                          system_instruction=system_prompt,
                                                          responseMimeType = "application/json",
                                                          responseSchema = DiabetesContext
                                                      ))

    resp = response.text
    return resp

## User input gets processed in a DiabetesContext conversation model
class DiabetesContext(BaseModel):

    ### 1. semantic 
    intent: Optional[str] = None  # e.g., "ask_how_to_log", "report", "complaint"
    unmapped_inputs: List[str] = Field(default_factory=list)

    ### 2. question 
    question_topic: Optional[str] = None
    question_type: Optional[str]= None
    unanswered_question_needs_answer: Optional[bool] = None
    
    ### 3. glucose measurement 
    glucose_level: Optional[float] = None
    glucose_unit: Optional[str] = None  # "mg/dL" or "mmol/L"
    measurement_time: Optional[str] = None

    ### 4. medication 
    medication_taken: Optional[bool] = None
    medication_name: Optional[str] = None

    ### 5. food 
    meal_type: Optional[str] = None          
    food_items: Optional[List[str]] = None  
    portion_size: Optional[str] = None       
    carbs_estimate: Optional[float] = None   
    calories_estimate: Optional[float] = None 
    time_of_eating: Optional[str] = None
    dietary_preferences: List[str] = Field(default_factory=list) 

    ### 6. physical activity 
    exercise: Optional[str] = None
    pysical_activity_preferences: List[str] = Field(default_factory=list)
    injury: Optional[str] = None
    physical_activity_barriers: Optional[str] = None

    ### 7. psychological 
    perceived_stress: Optional[str] = None
    mood: Optional[str] = None
    reason_for_mood: Optional[str] = None
    user_concerns: List[str] = Field(default_factory=list) 

    ### 8. identity 
    core_strengths: List[str] = Field(default_factory=list) 
    personal_values: List[str] = Field(default_factory=list)
    recent_success: Optional[str] = None 

    ### 9. barriers to self-management 
    emotional_barrier: Optional[str] = None       
    cognitive_barrier: Optional[str] = None      
    contextual_barrier: Optional[str] = None     
    behavioral_barrier: Optional[str] = None  

    ### 10. future-oriented behavioral goals 
    goal_area: Optional[str] = None    
    goal_reason: Optional[str] = None  

   

def reason_about_atomic_info(prompt, system_prompt):
    response = app.llm.client.models.generate_content(model="gemini-2.0-flash", 
                                                      contents=[prompt], 
                                                      config=types.GenerateContentConfig(
                                                          temperature = 0,
                                                          seed = 45362,
                                                          system_instruction=system_prompt,
                                                          responseMimeType = "application/json",
                                                          responseSchema = ReasoningResult
                                                      ))

    resp = response.text
    return resp

class ReasoningResult(BaseModel):
    response_type: Literal["ack", "answer", "question"]
    value: str 
    reason: str

class SoftSelfManagamentIndicators(BaseModel):
    soft_self_management_indicators: List[str] = Field(default_factory=list)

def reason_about_self_management(prompt, system_prompt):
    response = app.llm.client.models.generate_content(model="gemini-2.0-flash", 
                                                      contents=[prompt], 
                                                      config=types.GenerateContentConfig(
                                                          temperature = 0,
                                                          seed = 45362,
                                                          system_instruction=system_prompt,
                                                          responseMimeType = "application/json",
                                                          responseSchema = SoftSelfManagamentIndicators
                                                      ))

    resp = response.text
    return resp