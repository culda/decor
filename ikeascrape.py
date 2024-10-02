import requests
from bs4 import BeautifulSoup
import os
import json

def scrape_ikea_chairs(url):
    # Send a GET request to the URL
    response = requests.get(url)
    print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all product cards
    product_cards = soup.find_all('div', class_='plp-fragment-wrapper')

    print(product_cards)

    products = []

    for card in product_cards:
        product = {}

        # Extract product details
        product['name'] = card.find('span', class_='plp-price-module__product-name').text.strip()
        product['description'] = card.find('span', class_='plp-price-module__description').text.strip()
        product['price'] = card.find('span', class_='plp-price__integer').text.strip()

        # Extract image URLs
        image_tags = card.find_all('img', class_='plp-product__image')
        product['images'] = [img['src'].replace('?f=xxs', '') for img in image_tags]

        products.append(product)

    return products

def download_images(products, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for product in products:
        product_dir = os.path.join(output_dir, product['name'])
        if not os.path.exists(product_dir):
            os.makedirs(product_dir)

        for i, img_url in enumerate(product['images']):
            response = requests.get(img_url)
            if response.status_code == 200:
                filename = f"{product['name']}_{i+1}.jpg"
                with open(os.path.join(product_dir, filename), 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")

def main():
    url = "https://www.ikea.com/gb/en/cat/bar-stools-chairs-20864/"
    output_dir = "ikea_chair_images"

    products = scrape_ikea_chairs(url)
    download_images(products, output_dir)

    # Save product details to a JSON file
    with open('ikea_chairs_data.json', 'w') as f:
        json.dump(products, f, indent=2)

if __name__ == "__main__":
    main()
