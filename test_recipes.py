import pytest
from recipes import Ingredient
from recipes import Recipe
from recipes import ShoppingList
from recipes import DietaryRecipe


@pytest.fixture
def base_ingredient():
    return Ingredient(name="Мука", quantity=500.0, unit="г")


def test_ingredient_initialization(base_ingredient):
    assert base_ingredient.name == "Мука"
    assert base_ingredient.quantity == 500.0
    assert base_ingredient.unit == "г"


def test_ingredient_str(base_ingredient):
    assert str(base_ingredient) == "Мука: 500.0 г"


def test_same_name_and_unit_equal(base_ingredient):
    other_ingredient = Ingredient(name="Мука", quantity=100.0, unit="г")
    assert base_ingredient == other_ingredient


def test_different_names_unequal(base_ingredient):
    other_ingredient = Ingredient(name="Сахар", quantity=500.0, unit="г")
    assert base_ingredient != other_ingredient


def test_different_units_unequal(base_ingredient):
    other_ingredient = Ingredient(name="Мука", quantity=500.0, unit="кг")
    assert base_ingredient != other_ingredient
