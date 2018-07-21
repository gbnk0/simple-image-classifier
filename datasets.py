import os
from utils import make_dir, normalize_name, make_uuid

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
        result = False
        label_dir = self.datasets_dir + \
            normalize_name(dataset_name) + '/' + label_name

        make_dir(label_dir)
        filename = make_uuid() + '.jpg'
        filepath = label_dir + '/' + filename

        # if file passed in body
        if len(request.body) > 0:
            with open(filepath, 'wb') as file:
                file.write(request.body)
                result = True

        if 'json' in request.keys() and len(request.json) > 0:
            if 'url' in request.json:
                print('toto')
                result = True

        return result
