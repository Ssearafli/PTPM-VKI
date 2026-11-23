from abc import ABC, abstractmethod


class ExternalService(ABC):
    @abstractmethod
    def send(self, payload: str) -> bool:
        pass


class LoggingExternalService(ExternalService):

    def __init__(self):
        self.sent_messages = []

    def send(self, payload: str) -> bool:
        self.sent_messages.append(payload)
        return True