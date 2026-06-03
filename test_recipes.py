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


@pytest.fixture
def second_recipe(second_ingredient):
    return Recipe(title="КокаКоля", ingredients=[second_ingredient])


@pytest.fixture
def empty_shop_list():
    return ShoppingList()


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


#  Проверка класса ShoppingList
def test_add_recipe(empty_shop_list, base_recipe):
    empty_shop_list.add_recipe(base_recipe, portions=2)
    assert empty_shop_list._items[0][0].quantity == 1000
    assert empty_shop_list._items[0][1] == "Экспонента"


def test_add_recipe_incorrect_portions(empty_shop_list, base_recipe):
    try:
        empty_shop_list.add_recipe(base_recipe, portions=-1)
        assert False
    except ValueError:
        pass


def test_remove_recipe(empty_shop_list, base_recipe, second_recipe):
    empty_shop_list.add_recipe(base_recipe, portions=1)
    empty_shop_list.add_recipe(second_recipe, portions=1)
    empty_shop_list.remove_recipe("Экспонента")
    assert len(empty_shop_list._items) == 1


def test_get_list(empty_shop_list, base_ingredient, base_ingredient_same_name_and_unit, second_ingredient):
    recipe1 = Recipe(title="Приятный напиток", ingredients=[base_ingredient, second_ingredient])
    recipe2 = Recipe(title="ПочтиКокаКоля", ingredients=[base_ingredient_same_name_and_unit])
    empty_shop_list.add_recipe(recipe1, portions=1)
    empty_shop_list.add_recipe(recipe2, portions=1)
    final_shoppi_list = empty_shop_list.get_list()
    assert len(final_shoppi_list) == 2
    assert final_shoppi_list[0].name == "Вода"
    assert final_shoppi_list[1].name == "Мука"
    assert final_shoppi_list[1].quantity == 800.0


def test_add_method(base_recipe, second_recipe):
    listik1 = ShoppingList()
    listik2 = ShoppingList()
    listik2.add_recipe(second_recipe, portions=1)
    listik1.add_recipe(base_recipe, portions=1)
    combined_list = listik1 + listik2
    assert len(combined_list._items) == 2
    assert len(listik1._items) == 1
    assert len(listik2._items) == 1
