from enum import Enum, auto
from typing import Callable, List

class FeatureState(Enum):
    STANDARD = auto()
    EXPERIMENTAL = auto()

class Feature:
    def __init__(self, name: str, handler: Callable[[str], str], state: FeatureState):
        self.name = name
        self.handler = handler
        self.state = state

class FeatureManager:
    def __init__(self):
        self._features: List[Feature] = []

    def register(self, feature: Feature):
        self._features.append(feature)

    def build_pipeline(self, enable_experimental: bool) -> List[Callable[[str], str]]:
        pipeline: List[Callable[[str], str]] = []
        for f in self._features:
            if f.state == FeatureState.STANDARD:
                pipeline.append(f.handler)
            elif enable_experimental and f.state == FeatureState.EXPERIMENTAL:
                pipeline.append(f.handler)
        return pipeline
