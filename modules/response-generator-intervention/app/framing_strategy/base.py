from abc import ABC, abstractmethod
from app.util import ResponseType

class FramingStrategy(ABC):
    @abstractmethod
    def generate_response(self, context: dict, user_input: dict, response_type: ResponseType) -> str:
        pass

    @abstractmethod
    def generate_greeting(self, context: dict, user_input: dict) -> str:
        pass

    @abstractmethod
    def generate_closing(self, context: dict, user_input: dict) -> str:
        pass

    @abstractmethod
    def generate_advice(self, context: dict, user_input: dict) -> str:
        pass

    @abstractmethod
    def generate_question(self, context: dict, user_input: dict) -> str:
        pass