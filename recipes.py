class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.unit = unit
        self.quantity = quantity

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', '{self.quantity}', '{self.unit}')"

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title: str, ingredients: list):
        self.title = title
        self.ingredients = list(ingredients)

    def add_ingredient(self, ingredient: Ingredient):
        for ingredient_already_in in self.ingredients:
            if ingredient_already_in.name == ingredient.name and ingredient_already_in.unit == ingredient.unit:
                ingredient_already_in.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if type(ratio) in (int, float) and ratio > 0:
            return True
        return False

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Неправильный ratio, должно быть положительным числом")
        new_ingredients = []
        for ing in self.ingredients:
            new_quantity = ing.quantity * ratio
            new_ing = Ingredient(ing.name, new_quantity, ing.unit)
            new_ingredients.append(new_ing)
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = self.title + ":\n"
        for i in range(len(self.ingredients)):
            result += "  " + str(self.ingredients[i])
            if i != len(self.ingredients) - 1:
                result += "\n"
        return result








