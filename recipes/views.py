from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search_recipes(request):
    try:
        terms = request.GET.get('search')
        if (not terms):
            raise Exception('Error')

        recipes = Recipe.objects.filter(Q(
            Q(title__contains=terms) | Q(description__contains=terms)
            ), is_published=True)

        if (len(recipes) == 0):
            raise Exception('Error')

        return render(request, 'recipes/pages/recipes-view.html', context={
            'recipes': recipes,
            'code': 200,
            'terms': terms
        })
    except Recipe.DoesNotExist:
        return render(request, 'recipes/pages/recipes-view.html', context={
            'code': 404
        })
    except Exception as e:
        return render(request, 'recipes/pages/recipes-view.html', context={
            'code': 404,
            'error': e,
            'terms': terms
        })
