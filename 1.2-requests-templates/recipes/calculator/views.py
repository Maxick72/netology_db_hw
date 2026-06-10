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


def recipes_view(request, recipe_name):

    recipe_source = DATA.get(recipe_name)

    if not recipe_source:
        context = {'recipe': None}
        return render(request, 'calculator/index.html', context)

    servings = int(request.GET.get('servings', 1))

    res_recipe = {ingredient: amount * servings for ingredient, amount in recipe_source.items()}

    context = {
        'recipe': res_recipe
    }

    return render(request, 'calculator/index.html', context)