from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import json
from mistralai import Mistral
import os

api_key = os.getenv("api_key")
model = "open-mistral-7b"
mistral_client = Mistral(api_key=api_key)

encoder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(":memory:")

with open('products_with_recipes_and_ingredients.json', 'r', encoding='utf-8') as file:
    documents = json.load(file)
    
#print(documents[:2])

collection_name = 'my_recipes'

qdrant_client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE,
    ),
)

#print(f"Collection '{collection_name}' created successfully.")

qdrant_client.upload_points(
    collection_name=collection_name,
    points=[
        models.PointStruct(
            id=idx,
            vector=encoder.encode(", ".join(doc["Ingredients"])).tolist(),
            payload=doc
        )
        for idx, doc in enumerate(documents)
    ],
)

#print("Documents uploaded to Qdrant successfully!")

def retrieve_recipe(query):
    query_vector = encoder.encode(query).tolist()
    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=3
    )
    return search_results

def generate_response_with_rag(user_input):
    
    search_results = retrieve_recipe(user_input)
    #print(search_results)
    #print(type(search_results))
    
    final_results = []
    
    for result in search_results:
        recipe = result.payload.get('Recipe')
        
        #print(recipe)
        
        final_results.append(recipe)
        
    #print(final_results)

    prompt = (
        f"You are a National Foods chatbot, respond to user input accordingly.\n If the user asks about food or recipes, use the Knowledge:\n{final_results} to answer.\n If the user input is other than recipe or food, reply accordinly with your own knowledge.\n"
        )
    
    chat_response = mistral_client.chat.complete(
        model=model,
        messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
    )
    
    return chat_response.choices[0].message.content
    

"""while True:
    user_input = input("Assistant (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    response = generate_response_with_rag(user_input)
    print(f"AI response: {response}")"""
