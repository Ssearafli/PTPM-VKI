from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def get_input(self):
        pass


class ConsoleUserInterface(UserInterface):
    def get_input(self):
        side_a = input("Введите сторону A: ").strip()
        side_b = input("Введите сторону B: ").strip()
        side_c = input("Введите сторону C: ").strip()
        return side_a, side_b, side_c
