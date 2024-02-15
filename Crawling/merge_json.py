# This code merges the json files into one file.

import json
import os
from tqdm import tqdm

output_path = './datasets'
json_files = [f for f in os.listdir(output_path) if f.endswith('.json')]


# Merge the json files
item_urls = set() # To remove duplicates
item_list = []
image_id = 0
for json_file in json_files:
    with open(os.path.join(output_path, json_file), 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Get each codimap from the json file
        for codimap_dict in data:
            # Get items from each codimap
            current_item_list = codimap_dict['item_list']

            # Add item urls to item_list if they are not in item_urls
            for item in current_item_list:
                if item['image_url'] not in item_urls:
                    item_urls.add(item['image_url'])
                    item_list.append(item)

# Modify list to add image_id ({'000000': {item1}, '000001': {item2}, ...)
item_list = {str(i).zfill(6): item for i, item in enumerate(item_list)}

print(f"Number of items: {len(item_list)}")

# Check if there are any duplicates
set = {item['image_url'] for item in item_list.values()}
print(f"Number of unique items: {len(set)}")

# Save the merged json file
with open('merged.json', 'w', encoding='utf-8') as f:
    json.dump(item_list, f, ensure_ascii=False, indent=4)