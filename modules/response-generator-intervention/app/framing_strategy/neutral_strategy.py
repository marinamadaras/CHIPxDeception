from app.framing_strategy.base import FramingStrategy
from app.util import ResponseType
from app.util.ai_api_connector import generate

netural_system_prompt = "### Context ###\n" \
                        "You act the role of a medical chat-bot, who aids a diabetes patient with their self-management." \
                        "You will be given atomic pieces of information, about the patient and about medical science, " \
                        "which you will have to link together in a succint, straight to the point manner." \
                        "You should stay closely connexted to the context, be impartial, stick to factual communication, without adding inference or analysis."\
                        "The atomic pieces of information are going to be prefaced with a corresponding header.\n" \
                        "### Examples ###\n"\
                        "Example 1: Getting 7 to 9 hours of sleep is generally recommended for most adults. Would you like tips on improving your sleep routine?\n"\
                        "Example 2: Thanks for sharing. Persistent headaches can have several causes. Would you like to go through a few follow-up questions to narrow it down?"

class NeutralStrategy(FramingStrategy):

    # Delegates the generation of the prompt based on the expected response type
    def generate_response(self, context, user_input, response_type) -> str:
        
        if response_type == ResponseType.G:
            return self.generate_greeting(context, user_input)
        
        elif response_type == ResponseType.Q:
            return self.generate_question(context, user_input)
        
        elif response_type == ResponseType.A:
            hardcoded_context = {
                "user_goal": "exercise more regularly",
                "barrier": "lack of motivation in the morning",
                "past_success": "used to enjoy lunchtime walks",
                "value": "staying healthy for their kids"
            }
            # return self.generate_advice(hardcoded_context, user_input)
            return "You previously enjoyed lunchtime walks. You could consider adding them back into your routine."
            # return self.generate_advice(context, user_input)
        
        elif response_type == ResponseType.C:
            return self.generate_closing(context, user_input)

        return "'Sup homies"
    
    # Generates a greeting for the user
    def generate_greeting(self, context: dict, user_input: dict) -> str:
        try:
            name = user_input['patient_name']
        except KeyError:
            name = "Unknown patient"
        return f"Hi, {name}! I’m here to help you manage your diabetes. How can I assist you today?"
    
    # Generates a goodbye message for the user
    def generate_closing(self, context: dict, user_input: dict) -> str:
        try:
            name = user_input['patient_name']
        except KeyError:
            name = "Unknown patient"
        return f"Goodbye, {name}!"

    
    def generate_advice(self, context: dict, user_input: dict) -> str:
         ### TODO: figure out what activities I want and refine them
        # hardcoded_activity = "cycling"
        # hardcoded_activity = "lunchtime walks"
        prompt_activity = f"""The user talking to you is a diabetes patient.\n
                            ### Context ###\n
                            The context is: {context}.\n
                            ### Task ###\n
                            Formulate a suggestion with the given the past success for the diabetes patient."""

        return generate(prompt_activity , netural_system_prompt)
        # return f"Goodbye, !"
    
    def generate_question(self, context: dict, user_input: dict) -> str:
        ### TODO: figure out what contexts I want and refine them
        hardcoded_context_1 = "ate sugar today"
        hardcoded_context_2 = "ate cake today"
        hardcoded_context_3 = "has not worked out in 4 weeks"

        prompt_unfavorable_behavior = f"""The user talking to you is a diabetes patient.\n
                                        ### Context ###\n
                                        The context is: {hardcoded_context_1} and you would like to understand what led the patient to it, such that you can understand them better and help in their self-management.\n
                                        ### Task ###\n
                                        Formulate a question for the diabetes patient."""
        
        prompt_priorities = f"""The user talking to you is a diabetes patient.\n
                            ### Context ###\n
                            The context is: {hardcoded_context_2} and you would like to know their general values and how they prioritize them, in relationship to this context. That is because you currently know too little about them and you want to recommend activities that involve their values.\n
                            ### Task ###\n
                            Formulate a question for the diabetes patient."""
        
        prompt_physical_activities = f"""The user talking to you is a diabetes patient.\n
                            ### Context ###\n
                            The context is {hardcoded_context_3} and you would like to know what types of physical activities they enjoy doing, such that you can understand them better and recommend an activity they prefer. Mention it like an exploration.\n
                            ### Task ###\n
                            Formulate a question for the diabetes patient."""
        
        return generate(prompt_physical_activities , netural_system_prompt)
        # return f"Goodbye,!"

    # def formulate_question(query: str) -> str:
#     """
#     Formulates a natural language question based on which facts are missing from the DB.
#     """
#     if 'prioritizedOver' in query:
#         return "that depends on what you find important. What do you prioritize"
#     elif 'hasPhysicalActivityHabit' in query:
#         return "what physical activities do you regularly do"
#     raise ValueError(f"Cannot formulate question for query {query}")

# # =============================================================================
# # def formulate_advice(activity: str) -> str:
# #     prefix = "http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#"
# #     activity = activity.replace(prefix, "")
# # 
# #     activity = activity.replace("_", " ")
# #     return activity
# # =============================================================================


# def formulate_advice(activity: str) -> str:
#     prefix = "http://www.semanticweb.org/aledpro/ontologies/2024/2/userKG#"
#     activity = activity.replace(prefix, "")

#     # Split activity on underscore and take the last part if it starts with "activity"
#     parts = activity.split("_")
#     if parts[0] == "activity":
#         activity = "_".join(parts[1:])

#     activity = activity.replace("_", " ")
#     return activity
      
# netural_system_prompt = "You act the role of a medical chat bot, that " \
#                 "is able to link facts about the patient and about " \
#                 "medical science in order to give advice." \
#                 " You do not need to do this linking yourself as this will be given to" \
#                 " you if available. I will give you a context, and a message " \
#                 "typed by the user that is talking to you, both prefaced by " \
#                 "a corresponding header, and you will attempt to generate an " \
#                 "appropriate response to the user. " \
#                 "Your replies should be succinct, to the point," \
#                 " and not stray too far from the context."
