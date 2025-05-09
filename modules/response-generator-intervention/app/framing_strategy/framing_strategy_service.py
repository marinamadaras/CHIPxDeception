import importlib
from app.framing_strategy import FramingStrategy
from app.framing_strategy .neutral_strategy import NeutralStrategy
from app.framing_strategy .empathetic_strategy import EmpatheticStrategy

STRATEGY_MAP = {
    "neutral": NeutralStrategy,
    "empathetic": EmpatheticStrategy
}

class FramingStrategyService:
    strategy: FramingStrategy | None = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        strategy_name = app.config.get("FRAMING_STRATEGY")
        if not strategy_name:
            raise RuntimeError("FRAMING_STRATEGY must be set")

        strategy_class = STRATEGY_MAP.get(strategy_name.lower())
        if not strategy_class:
            raise ValueError(f"No strategy found for name '{strategy_name}'")
        
        self.strategy = strategy_class()
        app.extensions = getattr(app, "extensions", {})
        app.extensions["framing_strategy"] = self

    def get(self) -> FramingStrategy:
        if not self.strategy:
            raise RuntimeError("Strategy not initialized")
        return self.strategy

