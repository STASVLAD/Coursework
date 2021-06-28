from datetime import datetime, timedelta
from statistics import median
import numpy as np
from math import isclose


def suggest_freq(pfc):
    '''
    рекомендации для периодически покупаемых товаров
    '''
    recs = []

    freq_medians = {}
    for i in range(len(pfc)):
        freqs = np.array(pfc[i][1])
        freqs = freqs[freqs > timedelta(0)]
        if len(freqs) > 0:
            freq_medians[pfc[i][0]] = median(freqs)
        else:
            freq_medians[pfc[i][0]] = timedelta(0)

    # debug: datetime.now() : test = datetime.now() + timedelta(days=2)
    for product, freq, cron in pfc:
        if ((datetime.now() - cron).days >= freq_medians[product].days) and freq_medians[product].days != 0:
            recs.append(product)

    return recs


def custom_intersection(basket, ingredients):
    '''
    пересечение корзины с ингредиентами рецепта
    '''
    intersec = []
    for item in basket:
        for ingredient in ingredients:
            if item in ingredient.split():
                intersec.append(item)
                break
    return intersec


def eval_score(x, basket):
    '''
    score = len(intersection) / len(recipe)
    '''
    ingredients = set(x)
    intersection = custom_intersection(basket, ingredients)
    score = len(intersection) / len(ingredients)
    if isclose(score, 1, rel_tol=1e-5):
        score = -1
    return (score, set(intersection))


def suggest_recipes(df, basket):
    '''
    Рекомендация рецептов для пользователя 
    '''
    best_recipes = []
    for _ in range(5):
        scores = df['ingredients'].apply(eval_score, args=(basket,)).sort_values(ascending=False)
        best_ingredients = set(scores[0][1])
        best_recipes.append(scores.index[0])
        basket = basket - best_ingredients
        if len(basket) <= 1:
            break
    return best_recipes
