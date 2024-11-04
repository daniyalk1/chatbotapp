import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

urls = [
    'https://www.nfoods.com/our-food/recipe-mixes/',
    'https://www.nfoods.com/our-food/ingedients/',
    'https://www.nfoods.com/our-food/salt/',
    'https://www.nfoods.com/our-food/ketchup/',
    'https://www.nfoods.com/our-food/pickles/',
    'https://www.nfoods.com/our-food/mayonnaise/',
    'https://www.nfoods.com/our-food/desserts-jams-jellies/',
    'https://www.nfoods.com/our-food/jams/',
    'https://www.nfoods.com/our-food/chutneys-sauces-pastes/',
    'https://www.nfoods.com/our-food/seasonings/'
]

#   print(product_listings)

#print(categories)

combined_products = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    category_listings = soup.find_all('ul', class_='product-listing')
    
    categories = []
    for category_listing in category_listings:
        category = category_listing.find_previous('h3', class_='black-text').text.strip()
        categories.append(category)

    for idx, category_listing in enumerate(category_listings):
        product_names = category_listing.find_all('h6', class_='product-name')
        product_descriptions = category_listing.find_all('p', class_='small-para')
        product_images = category_listing.find_all('div', class_='product-img')
    
        for i in range(len(product_names)):
            name = product_names[i].text.strip()
            description = product_descriptions[i].text.strip() if i < len(product_descriptions) else 'No description'
        
            img_tag = product_images[i].find('img') if i < len(product_images) else None
            image_url = img_tag.get('data-src') or img_tag.get('src') if img_tag else 'No image'
        
            product_info = {
                'Category': categories[idx],
                'Product': name,
                'Description': description,
                'Image URL': image_url
            }
            combined_products.append(product_info)
        
df = pd.DataFrame(combined_products)

#print(df)

df.to_json('multiple_pages_products_data.json', orient='records', indent=4)

print("Data saved to multiple_pages_products_data.json")

"""for product in combined_products:
    print(product)"""
    


"""h3_above_product_listing = []

for category_listing in category_listings:
    for sibling in category_listing.find_all_previous('h3', class_='black-text'):
            h3_above_product_listing.append(sibling.text)
            break

h3_above_product_listing = list(dict.fromkeys(h3_above_product_listing))

product_names_lst = []

product_names = soup.find_all('h4', class_= 'black-text bold-text')
#print(product_names)

for product_name in product_names:
    product_names_lst.append(product_name.text)

product_descriptions_lst = []
for category_listing in category_listings:
    descriptions = category_listing.find_all('p', class_='small-para')
    for desc in descriptions:
        product_descriptions_lst.append(desc.text)
        
product_image_urls_lst = []
for category_listing in category_listings:
    product_imgs = category_listing.find_all('div', class_='product-img')
    for img_div in product_imgs:
        img_tag = img_div.find('img')
        
        if img_tag:
            img_url = img_tag.get('data-src')
            if img_url:
                product_image_urls_lst.append(img_url)"""


#print(len(h3_above_product_listing))
#print(len(product_names_lst))
##print(len(product_descriptions_lst))
#print(len(product_image_urls_lst))

"""combined_products = []
category_index = 0

for i in range(len(product_names_lst)):
    if i < len(product_names_lst):
        product_info = {
            'Product': product_names_lst[i],
            'Description': product_descriptions_lst[i],
            'Image URL': product_image_urls_lst[i],
            'Category': categories[category_index]
        }
        combined_products.append(product_info)
    
print(combined_products)"""



