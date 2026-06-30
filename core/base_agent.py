from abc import ABC, abstractmethod

from utils.logger import logger


class BaseAgent(ABC):

    def __init__(self, name: str):

        self.name = name

    def log(self, message):

        logger.info(f"[{self.name}] {message}")

    @abstractmethod
    def execute(self, state):

        pass