from abc import abstractmethod, ABC
from typing import Any


class Validator(ABC):
    def __set_name__(self, owner: "BurgerRecipe", name: str) -> None:
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: "BurgerRecipe",
            owner: "BurgerRecipe"
    ) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: "BurgerRecipe", value: int | str) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if not self.min_value <= value <= self.max_value:
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} "
                             f"and greater than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:

    cheese = Number(0, 2)
    buns = Number(2, 3)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(
            self,
            buns: int,
            cheese: int,
            tomatoes: int,
            cutlets: int,
            eggs: int,
            sauce: str
    ) -> None:
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.buns = buns
        self.sauce = sauce
