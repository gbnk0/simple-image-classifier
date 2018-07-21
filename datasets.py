import os
from utils import make_dir, normalize_name, make_uuid, save_from_url

class Datasets(object):

    def __init__(self, datasets_dir):
        self.datasets_dir = datasets_dir
        make_dir(datasets_dir)

    def get(self):
        results = []
        for folder in os.listdir(self.datasets_dir):
            dataset = {
                "name": folder,
                "labels": os.listdir(self.datasets_dir + folder + '/')
            }
            results.append(dataset)
        return results

    def create(self, name):
        result = False

        name = normalize_name(name)
        dataset_path = self.datasets_dir + name

        if make_dir(dataset_path):
            result = True

        return result
    
    def add_file(self, request, dataset_name, label_name):
        label_dir = self.datasets_dir + \
            normalize_name(dataset_name) + '/' + label_name

        make_dir(label_dir)
        filename = make_uuid() + '.jpg'
        filepath = label_dir + '/' + filename

        is_json = False
        if hasattr(request, 'json'):
            if 'url' in request.json.keys():
                is_json = True
                print('IS JSON: ', is_json)

        if is_json:
            if 'url' in request.json:
                save_from_url(request.json['url'], filepath)
                result = True

        # if file passed in body
        if len(request.body) > 0 and not is_json:
            with open(filepath, 'wb') as file:
                file.write(request.body)
                result = True
        
        return result
