from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        pass

    @abstractmethod
    def show_result(self, message: str) -> None:
        pass


class ConsoleUserInterface(UserInterface):
    def get_input(self, prompt: str) -> str:
        return input(prompt)

    def show_result(self, message: str) -> None:
        print(message)