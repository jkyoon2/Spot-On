import json
import os
import requests
from tqdm import tqdm

output_path = './images'

# Read the merged json file
with open('merged.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Download the images
if not os.path.exists(output_path):
    os.makedirs(output_path)

for image_id, item in tqdm(data.items()):
    image_url = item['image_url']
    image_path = os.path.join(output_path, f'{image_id}.jpg')
    if not os.path.exists(image_path):
        with open(image_path, 'wb') as f:
            f.write(requests.get(image_url).content)