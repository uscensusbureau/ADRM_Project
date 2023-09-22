# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 21:03:37 2023

@author: skhan2
"""

import json

def remove_duplicate_keys(input_dict):
    seen_keys = dict()
    output_dict = {}

    for key, value in input_dict.items():
        if key not in seen_keys:
            output_dict[key] = value
            seen_keys[key] = None

    return output_dict

file_path = 'C:/Users/skhan2/Desktop/farooq/KB_FM.json'  # Replace with the path to your JSON file
with open(file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

modified_data = remove_duplicate_keys(data)
output_file_path = 'C:\\Users\\skhan2\\Desktop\\farooq\\KB_FM.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.seek(0)
    json.dump(modified_data, output_file, indent=4)
    output_file.truncate()
print(f'Duplicate keys removed and saved to {output_file_path}')
print(f"Number of mappings in New KnowledgeBase is {len(modified_data)}")