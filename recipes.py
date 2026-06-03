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


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")

        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        new_items = []
        for item in self._items:
            if item[1] != title:
                new_items.append(item)

        self._items = new_items

    def get_list(self):
        working_dict = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in working_dict:
                working_dict[key] += ingredient.quantity
            else:
                working_dict[key] = ingredient.quantity

        result = []
        for key in working_dict.keys():
            result.append(Ingredient(key[0], working_dict[key], key[1]))

        result.sort(key=lambda ingredients: ingredients.name)
        return result

    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other.items
        return new_list











