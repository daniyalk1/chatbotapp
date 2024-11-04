from mistralai import Mistral
import json

api_key = "uAyQH2qjnN5Batgf1YDp24KB3BLKLHBK"
model = "open-mistral-7b"
client = Mistral(api_key=api_key)

with open('multiple_pages_products_data.json', 'r', encoding= 'utf-8') as f:
    products = json.load(f)
    
products_with_recipes_and_ingredients = []

for product in products:
    product_name = product['Product']
    
    prompt = f"What can I make using {product_name} from National Foods, give me one recipe with ingredients?"

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
            "role": "user",
            "content": prompt,
            },
            {
            "role": "system",
            "content": "you are a helpful assistant but be specific"
            }
        ]
    )
    
    recipe = chat_response.choices[0].message.content
    
    ingredient_extraction_question = f"From the following recipe, extract all the ingredients:\n\n{recipe}"
    
    ingredient_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": ingredient_extraction_question,
            },
            {
                "role": "system",
                "content": "You are a personal chef assistant. Just provide a list the ingredients mentioned in the recipe in points just the ingredients no extra text."
            },
        ]
    )
    
    ingredients = ingredient_response.choices[0].message.content.splitlines()
    
    ingredients = [ingredient.strip() for ingredient in ingredients if ingredient.strip()]
    
    product['Recipe'] = recipe
    product['Ingredients'] = ingredients
    
    products_with_recipes_and_ingredients.append(product)

with open('products_with_recipes_and_ingredients.json', 'w', encoding='utf-8') as f:
    json.dump(products_with_recipes_and_ingredients, f, ensure_ascii=False, indent=4)

print("Recipes for all products have been saved to recipes.json.")