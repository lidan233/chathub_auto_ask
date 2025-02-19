import json
import sys

def extract_titles(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Assuming the JSON contains a list of items with "title" field
        titles = []
        for item in data:
            if 'title' in item:
                titles.append(item['title'])
                
        return titles
        
    except FileNotFoundError:
        print(f"File {json_file} not found")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file {json_file}")
        return None

if __name__ == "__main__":
    
    input_file =  "/media/lida/softwares/QE/cvpr2020"
    output_file = input_file + "_titles.json"
    titles = extract_titles(input_file)
    
    if titles:
        output_file = 'titles.json'
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(titles, file, indent=2)
        print(f"Extracted {len(titles)} titles to {output_file}")