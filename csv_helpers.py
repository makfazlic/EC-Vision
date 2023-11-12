import csv
import requests
import uuid
import os

def get_csv_headers(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        return your_list[0]

def get_csv_column(csv_file, column):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        return [row[column] for row in your_list[1:]]
    
def save_urls_to_folder(image_urls, names):
    unique_out_folder = str(uuid.uuid4())
    os.mkdir(unique_out_folder)
    for i, (name, image_url) in enumerate(zip(names, image_urls)):
        success = False
        try :
            img_data = requests.get(image_url).content
            extension = image_url.split('.')[-1].lower()
            if extension != 'jpg' and extension != 'png' and extension != 'jpeg':
                raise Exception('Invalid extension')
            with open(f'{unique_out_folder}/{name}.{extension}', 'wb') as handler:
                handler.write(img_data)
            success = True
        except:
            success = False
        print(f'[{i+1}/{len(image_urls)}] {"✅" if success else "🚫"}: {image_url}')
    return unique_out_folder

        

    
