# Reasoner
| Properties    |                        |
| ------------- |------------------------|
| **Name**      | Intervention Reasoning |
| **Type**      | Reasoner               |


## Description
This reasoner was developed to support conversations in the context of the BSc Project **To deceit or self-deceit?**
Most of the logic was **copied** from the `reasoning-demo` module, and then adapted for the use-case. 

## Pre-requisites for Setup
1. Make sure to have obtained [an API key for Gemini](https://ai.google.dev/gemini-api/docs/api-key), and set the `GEMINI_API_KEY` environment variable in the module's `config.env` to it
2. Configure `core-modules.yaml` to use this module as the response generator.

### Input from `Triple Extractor`
```JSON
{
    "sentence_data": {
        "patient_name": <string>,   // The name of the user currently chatting
        "sentence": <string>,       // The raw input that the user submitted
        "timestamp": <string>       // The time at which the user submitted the sentence (ISO format)
    },
    "triples": [                    // This part is ignored by the reasoner, but was kept from the cloned module
        {
            "subject":<string>, 
            "object": <string>, 
            "predicate":<string>
        },
        ...
    ]
}
```
### Output to `Response Generator`
```JSON
	{
        "sentence_data": {
            "patient_name": <string>,   // The name of the user currently chatting.
            "sentence": <string>,       // The sentence that the user submitted.
            "timestamp": <string>       // The time at which the user submitted the sentence (ISO format).
        },
  
        "type": <string>,               // The type of response being generated, corresponds to "response_type" in the data.
        "data":                         // The data to be used by the response generator.
            {                     
              "response_type": <string>,                       // The type of response to be generated, one of ack, question, answer, greeting, closing.
              "value": <string>,                               // The content that the response should contain, as atomic as possible.
              "reason": <string>,                              // The LLM's justification for the given response.
              "soft_self_management_indicators": [<string>],   // A list of inferred indicators that might indicate struggle with self-management.
              "personal_values": [<string>]                    // A list of personal values that the user has expressed in (previous) conversations.
            }       
	}
```

## Diabetes Context
To facilitate the conversations, the user input gets mapped to a `DiabetesContext` model, with fields relevant to managing diabetes. 

```Python
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

```

## Internal Dependencies
None.

## Required Resources
- Internet connection
- Gemini API Key