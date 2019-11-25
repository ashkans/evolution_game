def check_eat(pop, foods):
    for c in pop.creatures:
        for food in foods.contents:
            if pop.creatures[c].x + pop.creatures[c].size > food.x - food.size:
                if pop.creatures[c].x - pop.creatures[c].size < food.x + food.size:
                    if pop.creatures[c].y + pop.creatures[c].size > food.y - food.size:
                        if pop.creatures[c].y - pop.creatures[c].size < food.y + food.size:
                            food.eaten_by.append(c)
