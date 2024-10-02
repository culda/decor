import os
import json
import shutil
from PIL import Image

def build_lora_dataset(source_dir, output_dir, min_size=512):
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create images directory within output directory
    images_dir = os.path.join(output_dir, 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Load product data
    with open('ikea_chairs_data.json', 'r') as f:
        products = json.load(f)

    dataset = []

    for product in products:
        product_dir = os.path.join(source_dir, product['name'])
        if not os.path.exists(product_dir):
            continue

        for i, image_file in enumerate(os.listdir(product_dir)):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                source_path = os.path.join(product_dir, image_file)
                
                # Open image and check size
                with Image.open(source_path) as img:
                    width, height = img.size
                    if width < min_size or height < min_size:
                        print(f"Skipping {image_file} - too small")
                        continue

                # Create a unique filename
                new_filename = f"{product['name'].replace(' ', '_')}_{i+1}.jpg"
                dest_path = os.path.join(images_dir, new_filename)

                # Copy image to dataset directory
                shutil.copy2(source_path, dest_path)

                # Add metadata to dataset
                dataset.append({
                    'file_name': new_filename,
                    'text': f"An IKEA chair named {product['name']}, {product['description']}",
                    'metadata': {
                        'price': product['price'],
                        'product_name': product['name'],
                        'description': product['description']
                    }
                })

    # Save dataset metadata
    with open(os.path.join(output_dir, 'metadata.jsonl'), 'w') as f:
        for item in dataset:
            f.write(json.dumps(item) + '\n')

    print(f"Dataset built with {len(dataset)} images.")

if __name__ == "__main__":
    source_dir = "ikea_chair_images"
    output_dir = "ikea_chairs_lora_dataset"
    build_lora_dataset(source_dir, output_dir)
