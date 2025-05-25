import json
import copy
import re
from typing import Optional, List
from typing import Dict, Any, Optional
from flask import current_app
from app.util.ai_api_connector import DiabetesContext, process_input, reason_about_atomic_info, reason_about_self_management

mapping_user_input_system_prompt = """
### Role

You are an NLU module in a diabetes support chatbot.
Your task is to extract structured information from a user's message and populate a JSON object following the DiabetesContext schema.

---

### Instructions

- You will receive a raw user message as input.
- Populate as many fields as possible based on the message content.
- Fields should be populated with the most granular and self-contained values possible.

---

### Output

- Return a full JSON object. Use `null` for any field you cannot determine — do not omit keys.
- Always populate the semantic field:
    - **intent**: the user’s primary goal or communicative act (e.g., "log", "ask_for_exercise_advice", "express_stress").

--- 

### Field Types

The schema contains 10 types of fields:

    1. **semantic**: 
        - `intent`, `unmapped_inputs`

    2. **question**:
        -  `question_topic`, `question_type`, `unanswered_question_needs_answer`

    3. **glucose measurment**: 
        - `glucose_level`, `glucose_unit`, `measurment_time`

    4. **medication**: 
        - `medication_taken`, `medication_name`

    5. **food**: 
        - `meal_type`, `food_items`, `portion_size`, `carbs_estimate`, `calories_estimate`, `time_of_eating`, `dietary_preferences`

    6. **physical activity**:
        - `exercise`, `pysical_activity_preferences`, `injury`, `physical_activity_barriers`

    7. **psychological**: 
        - `perceived_stress`, `mood`, `reason_for_mood`, `user_concerns`

    8. **identity**:
        - `core_strengths`, `personal_values`, `recent_success`

    9. **barriers to diabetes self-management**:
        - `emotional_barrier`, `cognitive_barrier`, `contextual_barrier`, `behavioral_barrier`

    10. **future-oriented behavioral goals**: 
        - `goal_area`, `goal_reason`

---
    
### Special Handling for Questions

If the user is asking a question, also always populate all 3:
    - `question_topic`: The main subject of the question (e.g., "logging glucose").
    - `question_type`: The type of question (e.g., "how").
    - `unanswered_question_needs_answer`: set to `true`.

If the user is not asking a question, set all question-related fields to `null`.

---

### Ambiguity and Unmapped Content
    - If none of the fields match, or they do not match very well, store an atomic version of the user input in **unmapped_inputs**.

        """

reasoning_system_prompt = """
### Role

You are a structured reasoning module in a diabetes support chatbot. 

You receive as input:
	1.	A structured knowledge base representing the current known and inferred user state (across 10 field types)
	2.	A list of recently changed fields, reflecting updates to that knowledge base

Your task is to reason over this information and determine the system’s next action.

You must decide whether to:
	- acknowledge the user’s input (ack)
	- answer a question they asked (answer)
	- ask for more information (question)

Your output must be a structured representation composed of atomic units, describing what the system should do next.

---

### Input

1. `structured knowledge base` — long-term and current information about the user, organized into these 10 field types:

    1. **semantic**: 
        - `intent`, `unmapped_inputs`

    2. **question**: 
        - `question_topic`, `question_type`, `unanswered_question_needs_answer`

    3. **glucose measurment**:
        - `glucose_level`, `glucose_unit`, `measurment_time`

    4. **medication**: 
        - `medication_taken`, `medication_name`

    5. **food**: 
        - `meal_type`, `food_items`, `portion_size`, `carbs_estimate`, `calories_estimate`, `time_of_eating`, `dietary_preferences`

    6. **physical activity**:
        - `exercise`, `pysical_activity_preferences`, `injury`, `physical_activity_barriers`

    7. **psychological**: 
        - `perceived_stress`, `mood`, `reason_for_mood`, `user_concerns`

    8. **identity**:
        - `core_strengths`, `personal_values`, `recent_success`

    9. **barriers to diabetes self-management**: 
        - `emotional_barrier`, `cognitive_barrier`, `contextual_barrier`, `behavioral_barrier`

    10. **future-oriented behavioral goals**: 
        - `goal_area`, `goal_reason`

2. `recently_changed_fields` —  fields updated in the most recent user turn.
Focus your reasoning primarily on these. Use them to guide your decision on how to respond, while still considering the full knowledge base and long-term self-management goals.

---

### Decision Principles – **response_type**

Balance between ack, answer, and question, with a focus on clarity and progress toward better diabetes self-management.

- Choose **answer** when:
    - `unanswered_question_needs_answer` field is true
    - If context is partial, give a minimal but relevant answer.

- Choose **ack** when:
    - The user input is an update that:
        - Completes a field or set of related fields (e.g., food item + portion + time = full log)
        - Does not require further clarification for accurate interpretation or system reasoning
    - The input relates to a sensitive or personal topic (e.g., mood, barriers, values) and:
        - The system has sufficient context to understand the update
        - It is preferable to hold space unless the user shows readiness to elaborate

- Choose **question** when:
    - `unmapped_inputs` field is not empty
    - Any `recently_changed_field` is incomplete, ambiguous, or lacks required subfields for accurate logging of a key clinical or behavioral factor (e.g., glucose level without time, food item without time of eating)
    - Key information is still missing to reason about the user’s behavior, risks, or support needs — even after the most recent update
    - Prompting about identity, barriers, or goals could meaningfully advance understanding or support (e.g., if goals are set but goal_reason is still unknown)

Do not ask follow-up questions if the user’s input appears complete or relates to a sensitive topic already acknowledged by the system. Default to ack in those cases.

---

### Decision Principles - **value**

The value field represents the system’s atomic next step and must align with the selected response_type.

Use the following principles to determine what value to generate:

If response_type is answer:
- Base the answer direction on `question_type`, `question_topic` and `intent`.
- When available, use prior context to help refine the answer and increase its relevance to the user’s situation.
- Output a single, self-contained fact, action, or recommendation in natural language.
- The answer should be actionable or informative and stand on its own.

- Good Example: "Insert a test strip into your glucose meter."
- Bad Example: "You should walk because it lowers stress and helps weight loss."

If response_type is ack:
- Use a controlled semantic tag in the format ack_<topic> to represent the intention of the acknowledgment.
- Focus on recognizing user input in a way that conveys validation, or support.

If response_type is question:
- Use a controlled semantic tag in the format ask_<topic> or explore_<concept> to indicate what the system should inquire about.
- The tag must reflect a single conversational goal (e.g., ask_food_timing, explore_goal_motivation).
- Prioritize tags that help fill knowledge gaps or encourage user reflection on identity, values, or behavior change.

Always ensure value expresses one clear intention that downstream NLG components can render fluently and contextually.

---

### Decision Principles - **reason**

The reason field provides a concise, structured justification for why the current response_type and value were selected.

Use the following principles when generating the reason:
- Focus on the user’s most recent input as the main trigger
- Preserve specific user language, field-level references, or behavioral cues
- Include relevant prior context (e.g., missing values, patterns, goals) only when it directly informs the response
- Be specific and situational — avoid generic or meta-level explanations
- Do not describe what the system is doing — that is already captured by response_type and value
- Use a single, compact clause

Examples (preserve context + justification):
- "user reported low mood after skipping lunch"
- "glucose value logged but no measurment time provided"
- "user set a physical activity goal without stating motivation"
- "mentioned difficulty staying active due to pain"

What to avoid:
- Meta-commentary: "The user mentioned overeating, which is a sensitive topic, and the system acknowledges it"
- Overgeneralization: "user input unclear"
- Restating the value: "asking about food timing" 


Think of reason as a snapshot of the situation, not a description of the system’s behavior.

---

### Output

Your output has three parts:

1. `response_type`: A string that specifies the type of system action. Must be one of:
    - `ack`: acknowledge user input.
    - `answer`: respond to a user question. 
    - `question`: ask a clarifying or exploratory question.
    
2. `value`: The system’s atomic next step:

3. `reason`: A brief and concise natural-language explanation for the selected `response_type` and `value`. Must reference the user's most recent input and, if relevant, draw on prior context.


"""

self_management_system_prompt = """
### Role

You are a reasoning assistant that detects soft indicators of potential self-management difficulties in people managing diabetes.

You will receive a short, raw user input (usually a single sentence or phrase).  
Your task is to identify one or more soft self-management indicators if the phrasing suggests emotional, motivational, or psychological struggle.

These indicators are **not diagnoses or facts** — they are **tentative, low-confidence signals** that may suggest shame, guilt, low self-control, frustration, or related challenges.  
Do not make strong assumptions. Only output what the phrasing reasonably suggests.

---

### Focus Areas

- shame  
- guilt  
- discomfort  
- distress  
- low self-control  
- poor self-esteem  
- embarrassment  
- frustration  
- low self-efficacy  
- low self-compassion  

These are **common focus areas**, but **you are not limited to this list**.  

You may generate other relevant tags if they are:
- clearly supported by the user’s phrasing
- emotionally or motivationally meaningful

---

### Input

You will receive a raw user message as input.

---

### Output

A JSON object with a list of atomic tags:

{
    "soft_self_management_indicators": ["tag1", "tag2", ...]
}

---

### Example 1:

Input:
"I messed up again — I had so much sugar and now I feel awful."

Output:
{
    "soft_self_management_indicators": ["guilt", "shame", "low self-control"]
}

---
### Example 2:

Input:
"I didn’t bother checking my glucose today. What’s the point?"

Output:
{
    "soft_self_management_indicators":  ["low self-efficacy", "distress"]
}

---

### Example 3:

Input:
"Had oatmeal for breakfast, salad for lunch."

Output:
{
    "soft_self_management_indicators":  []
}

"""

GREETINGS = {
    "hi",
    "hello", 
    "hey", 
    "good morning", 
    "good night"}

CLOSING = (
    "bye",
    "thanks",
    "thank you",
    "goodbye"
)

class LightweightReasoner:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.turn_count = 0
        self.past_context: Optional[DiabetesContext] = None
        self.build_up_context: Optional[DiabetesContext] = None
        self._last_diff_fields: List[str] = []

        app.extensions = getattr(app, "extensions", {})
        app.extensions["reasoner"] = self

    
    ## This is the delegator of the reasoning logic
    ## 1. it first processes the raw user input
    ## 2. it then manages the state 
    ## 3. it then reasons over the current and past context to know what to tell the user
    def process_input(self, user_input: str) -> Dict[str, Any]:
        self.turn_count += 1
        
        # pre-processing (i don't make unnecessary calls to the LLM, if it's only a greeting)
        text = user_input.lower()

        if any(re.search(rf'\b{re.escape(greet)}\b', text, re.IGNORECASE) for greet in GREETINGS):
            return {"data": {}, "type": "greeting"}
        elif any(re.search(rf'\b{re.escape(close)}\b', text, re.IGNORECASE) for close in CLOSING):
            return {"data": {}, "type": "closing"}
        if text == "restart":
            self.build_up_context = None
            return {"data": {}, "type": "greeting"}
        if text in GREETINGS:
            return {"data": {}, "type": "greeting"}
        elif text in CLOSING:
            return {"data": {}, "type": "closing"}  
        
        
        ## 1. this part processes user-input and gets a partially filled out DiabetesContext object
        user_context = self.understand_user_input(user_input)
        # current_app.logger.info(f"CONTEXT!!!!: {user_context}")

        ## 2. this part adds to the in-memory context of the conversation, so the convo does not feel like disjoint messages
        self.manage_conversation_state(user_context)
        current_app.logger.info(f"BUILD UP CONTEXT!!!!: {self.build_up_context}")

        ## 3. this part is the reasoner actually, and it gets the atomic data for the response generator
        reasoning_result = self.reason_about_atomic_response()
        response_type = self.get_response_type(reasoning_result)

        soft_self_management_indicators = self.reason_about_soft_self_management_indicators(text)

        reasoning_result["soft_self_management_indicators"] = soft_self_management_indicators["soft_self_management_indicators"]
        reasoning_result["personal_values"] = self.build_up_context.personal_values

        self.build_up_context.unmapped_inputs = []
        self.build_up_context.unanswered_question_needs_answer = None
        
        current_app.logger.info(f"CONTEXTTTTT {reasoning_result}")
        return {
            "data": reasoning_result,
            "type": response_type
        }
    

    def understand_user_input(self, user_input):
        prompt = f"""
                Extract the relevant information from user input into a structured JSON object following the DiabetesContext schema.
                User Input: "{user_input}"
                """
        raw_user_context = process_input(prompt, mapping_user_input_system_prompt)
        user_context = DiabetesContext(**json.loads(raw_user_context))

        return user_context
    
    # This method is used to create the in-memory context of the entire conversation, 
    # by creating a general conversation Diabetes Context that gets updated each turn
    # and then making a diff to see what fields were "freshly" added 
    def manage_conversation_state(self, user_context):
        if self.build_up_context is None:
            self.build_up_context = copy.deepcopy(user_context)
        else:
             self._update_build_up_context(user_context)

        self._last_diff_fields = (
            self._compute_diff_fields(user_context, self.past_context)
            if self.past_context else []
        )

        self.past_context = copy.deepcopy(user_context)
    

    def reason_about_atomic_response(self) -> Dict[str, Any]:
        if self.build_up_context is None:
            return {"response_type": "",
                    "field_type": "",
                    "value": "",
                    "reason": ""}
        
    
        
        question_prompt = f"""
            ### CONTEXT:
            You are reasoning over structured user data related to diabetes.

            Here is the current `structured knowledge base`:
            {json.dumps(self.build_up_context.dict(), indent=2)}

            Since the last turn, this is the `list of recently changed fields`:
            {json.dumps(self._last_diff_fields)}

            ### TASK:
            Based on this context, output a single structured reasoning item that describes the system’s next action.
            """

        raw = reason_about_atomic_info(question_prompt, system_prompt=reasoning_system_prompt)
        return json.loads(raw)
    
    def reason_about_soft_self_management_indicators(self, text: str):
        raw = reason_about_self_management(f"The user's input is: {text}", self_management_system_prompt)
        return json.loads(raw)
        
    def _update_build_up_context(self, new_context: dict):
        for field, new_value in new_context.model_dump().items():
            if new_value not in [None, [], "", {}]:
                setattr(self.build_up_context, field, new_value)

    def _compute_diff_fields(self, current: DiabetesContext, previous: DiabetesContext) -> List[str]:
        diff = []
        for field in current.model_dump().keys():
            new_val = getattr(current, field)
            old_val = getattr(previous, field)
            if new_val != old_val and new_val not in [None, [], "", {}]:
                diff.append(field)
        return diff
    
    def get_response_type(self, response: dict):
        rt = response.get("response_type")
        if rt == "ack":
            return "ack"
        elif rt == "answer":
            return "answer"
        elif rt == "question":
            return "question"
        else:
            return "error"