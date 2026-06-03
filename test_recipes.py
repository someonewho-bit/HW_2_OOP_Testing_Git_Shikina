import pytest
from recipes import Ingredient
from recipes import Recipe
from recipes import ShoppingList
from recipes import DietaryRecipe


# Создание фикстур
@pytest.fixture
def base_ingredient():
    return Ingredient(name="Мука", quantity=500.0, unit="г")


@pytest.fixture
def base_ingredient_same_name_and_unit():
    return Ingredient(name="Мука", quantity=300.0, unit="г")


@pytest.fixture
def second_ingredient():
    return Ingredient(name="Вода", quantity=1.0, unit="л")


@pytest.fixture
def base_recipe(base_ingredient):
    return Recipe(title="Экспонента", ingredients=[base_ingredient])


# Проверка класса Ingredient
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


# Проверка класса Recipe
def test_recipe_initialization(base_ingredient, second_ingredient):
    recipe = Recipe(title="Приятный напиток", ingredients=[base_ingredient, second_ingredient])
    assert recipe.title == "Приятный напиток"
    assert recipe.ingredients[0] == base_ingredient
    assert recipe.ingredients[1] == second_ingredient


def test_add_ingredient(base_recipe, second_ingredient):
    base_recipe.add_ingredient(second_ingredient)
    assert len(base_recipe.ingredients) == 2
    assert base_recipe.ingredients[1].name == "Вода"


def test_add_duplicate_ingredient(base_recipe, base_ingredient_same_name_and_unit):
    base_recipe.add_ingredient(base_ingredient_same_name_and_unit)
    assert len(base_recipe.ingredients) == 1
    assert base_recipe.ingredients[0].quantity == 800  # 500 + 300


def test_scale_multiplication(base_recipe):
    ratio = 3
    new_scaled_recipe = base_recipe.scale(ratio)
    assert new_scaled_recipe.ingredients[0].quantity == 1500  # 500 * 3


def test_scale_return(base_recipe):
    ratio = 3
    new_scaled_recipe = base_recipe.scale(ratio)
    assert base_recipe.ingredients[0].quantity == 500  # сохранился и не умножится на 3


def test_ratio_error(base_recipe):
    ratio = -1
    try:
        base_recipe.scale(ratio)
        assert False
    except ValueError:
        pass


def test_recipe_len(base_recipe, second_ingredient):
    assert len(base_recipe) == 1
    base_recipe.add_ingredient(second_ingredient)
    assert len(base_recipe) == 2



