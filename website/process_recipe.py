def process_recipe(recipe):
    # Remove "Cooking Assistant:" and any leading/trailing whitespace
    processed_recipe = recipe.replace("<b>Cooking Assistant:</b>", "").strip()
    processed_recipe = processed_recipe.replace('<br><button class="btn btn-success mt-2" onclick="save_recipe(this.parentElement)">Save Recipe</button>', '')
    
    return processed_recipe 