import os
from utils import make_dir, normalize_name, make_uuid, save_from_url, save_from_bytes

def is_trained(dataset_path):
    result = False
    if os.path.isfile(dataset_path + 'retrained_labels.txt'):
        if os.path.isfile(dataset_path + 'retrained_graph.pb'):
            result = True
    return result

class Datasets(object):

    def __init__(self, datasets_dir):
        self.datasets_dir = datasets_dir
        make_dir(datasets_dir)

    def get(self, **kwargs):

        name = kwargs.get('name', None)
        results = []

        for dataset_name in os.listdir(self.datasets_dir):
            dataset_path = self.datasets_dir + dataset_name + '/'
            labels_path = dataset_path + 'labels'

            if os.path.isdir(dataset_path):
                labels = []
                for label in os.listdir(labels_path):
                    label_path = dataset_path + 'labels/' + label

                    if os.path.isdir(label_path):
                        labels.append(label)

                dataset = {
                    "name": dataset_name,
                    "labels": labels,
                    "path": dataset_path,
                    "trained": is_trained(dataset_path)
                }
                if name:
                    name = normalize_name(name)
                    if dataset_name == name:
                        return dataset

                results.append(dataset)
        return results


    def create(self, name):
        result = False

        name = normalize_name(name)
        dataset_path = self.datasets_dir + name
        
        subdirs = ['/bottlenecks', '/labels']
        if make_dir(dataset_path):
            for folder in subdirs:
                make_dir(dataset_path + folder)
            result = True

        return result
    
    def add_file(self, request, dataset_name, label_name):

        result = False
        request_json = {}
        label_dir = self.datasets_dir + \
            normalize_name(dataset_name) + '/' + 'labels/' + label_name

        make_dir(label_dir)

        filename = make_uuid() + '.jpg'
        filepath = label_dir + '/' + filename

        # if url passed to json body
        try:
            request_json = request.json
        except Exception as e:
            print(e)

        if 'url' in request_json.keys():
            save_from_url(request_json['url'], filepath)
            result = True

        # if file passed in body
        else:
            save_from_bytes(request.body, filepath)
            result = True
        
        return result
