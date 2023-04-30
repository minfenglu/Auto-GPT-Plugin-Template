import http.client
import json
import os

def api_key_set() -> bool:
    return True if os.getenv("SPOONACULAR_API_KEY") else False

def search_recipes(query: str) -> str:
    conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")
    headers = {
        'content-type': "application/octet-stream",
        'X-RapidAPI-Key': os.getenv("SPOONACULAR_API_KEY"),
        'X-RapidAPI-Host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    conn.request("GET", f"/recipes/complexSearch?query={query}&offset=0&number=10&", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    response_json = json.loads(data)
    results = response_json["results"] 
    prev_title = None
    idx = 1
    recipes = []
    for result in results:
        title = result["title"]
        id = result["id"]
        if prev_title != title:
            idx = 1
            recipe = f'{id}, {title}'
        else:
            idx += 1
            recipe = f'{id}, {title}_{idx}'
        print(recipe)
        recipes.append(recipe)
        prev_title = title
    return recipes

def get_analyzed_recipe_instructions(recipe_id: int) -> str:
    conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")
    headers = {
        'content-type': "application/octet-stream",
        'X-RapidAPI-Key': os.getenv("SPOONACULAR_API_KEY"),
        'X-RapidAPI-Host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    conn.request("GET", f"/recipes/{recipe_id}/analyzedInstructions?stepBreakdown=true", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    #data = '[{"name":"","steps":[{"number":1,"step":"Heat the oil in a pan. Grate the onion and the garlic into it.","ingredients":[{"id":11215,"name":"garlic","localizedName":"garlic","image":"garlic.png"},{"id":11282,"name":"onion","localizedName":"onion","image":"brown-onion.png"},{"id":4582,"name":"cooking oil","localizedName":"cooking oil","image":"vegetable-oil.jpg"}],"equipment":[{"id":404645,"name":"frying pan","localizedName":"frying pan","image":"pan.png"}]},{"number":2,"step":"Add the grated ginger as well.","ingredients":[{"id":11216,"name":"ginger","localizedName":"ginger","image":"ginger.png"}],"equipment":[]},{"number":3,"step":"Let it saut for 2 mins.","ingredients":[],"equipment":[],"length":{"number":2,"unit":"minutes"}},{"number":4,"step":"Add in the turmeric powder, coriander powder, cumin powder and kashmiri mirch and saut for a couple more minutes.","ingredients":[{"id":1002013,"name":"ground coriander","localizedName":"ground coriander","image":"ground-coriander.jpg"},{"id":2043,"name":"turmeric","localizedName":"turmeric","image":"turmeric.jpg"},{"id":1012014,"name":"ground cumin","localizedName":"ground cumin","image":"ground-cumin.jpg"}],"equipment":[]},{"number":5,"step":"Add the kasuri methi and the tomato paste mixed in water.","ingredients":[{"id":11887,"name":"tomato paste","localizedName":"tomato paste","image":"tomato-paste.jpg"},{"id":98963,"name":"dried fenugreek leaves","localizedName":"dried fenugreek leaves","image":"methi.png"},{"id":14412,"name":"water","localizedName":"water","image":"water.png"}],"equipment":[]},{"number":6,"step":"Add some more water if required.","ingredients":[{"id":14412,"name":"water","localizedName":"water","image":"water.png"}],"equipment":[]},{"number":7,"step":"When it starts to boil, add the salt and paneer cubes.","ingredients":[{"id":98847,"name":"paneer","localizedName":"paneer","image":"paneer.png"},{"id":2047,"name":"salt","localizedName":"salt","image":"salt.jpg"}],"equipment":[]},{"number":8,"step":"Let it cook in the gravy for a couple of minutes.","ingredients":[{"id":6997,"name":"gravy","localizedName":"gravy","image":"gravy.jpg"}],"equipment":[]},{"number":9,"step":"Add the cream and sugar and mix well. Dont let it boil after you have added the cream, just simmer for 15 minutes or so.","ingredients":[{"id":1053,"name":"cream","localizedName":"cream","image":"fluid-cream.jpg"},{"id":19335,"name":"sugar","localizedName":"sugar","image":"sugar-in-bowl.png"}],"equipment":[],"length":{"number":15,"unit":"minutes"}}]}]'
    instructions = json.loads(data)
    for instruction in instructions:
        name = instruction["name"]
        print("==== Recipe from Chef Minfeng ====")
        if name:
            print("====", name, "====")
        steps = instruction["steps"]
        for step in steps:
            ingredients = []
            equipments = []
            for ingredient in step["ingredients"]:
                ingredients.append(ingredient["name"])
            for equipment in step["equipment"]:
                equipments.append(equipment["name"])

            step_detail = f'    • step {step["number"]}: {step["step"]}'
            if ingredients:
                step_detail += f'\n        required ingredients: {",".join(ingredients)}'
            if equipments:
                step_detail += f'\n        required equipments: {",".join(equipments)}'
            step_detail += "\n"
            print(step_detail)
    return step_detail