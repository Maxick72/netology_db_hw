from logging import exception

from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:

def recipes_view(request, dish):
    try:
        recipe_dish = DATA[dish]
        quantity_dish = int(request.GET.get('servings', 1))
        res_recipe = {}
        for ing,amount in recipe_dish.items():
            if quantity_dish:
                res_recipe[ing] = amount * quantity_dish

        context = {
            'recipe': res_recipe
        }
        return render(request, 'calculator/index.html', context)
    except KeyError:
        context = {'recipe': None}
        return render(request, 'calculator/index.html', context)