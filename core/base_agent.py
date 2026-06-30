from abc import ABC, abstractmethod
from time import perf_counter


class BaseAgent(ABC):

    def __init__(self, name: str):
        self.name = name

    def log(self, message: str):
        print(f"[{self.name}] {message}")

    def measure(self, fn, state):

        start = perf_counter()

        state = fn(state)

        elapsed = round(
            (perf_counter() - start) * 1000,
            2,
        )

        if not hasattr(state, "agent_metrics"):
            state.agent_metrics = {}

        state.agent_metrics[self.name] = elapsed

        return state

    @abstractmethod
    def execute(self, state):
        pass