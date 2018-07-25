import os
import time
from utils import make_dir, normalize_name, save_from_urls, save_from_bytes

def is_trained(dataset_path):
    result = False
    if os.path.isfile(dataset_path + 'retrained_labels.txt'):
        if os.path.isfile(dataset_path + 'retrained_graph.pb'):
            result = True
    return result

def get_labels(dataset_path):
    labels = []
    labels_path = dataset_path + 'labels'
    if os.path.isdir(dataset_path):
        for label_name in os.listdir(labels_path):
            label_path = dataset_path + 'labels/' + label_name

            if os.path.isdir(label_path):
                label_data = {
                    "name": label_name,
                    "items": len(os.listdir(label_path))
                }
                labels.append(label_data)
    return labels

def last_trained_date(dataset_path):
    result = 'never'
    graph_file = dataset_path + 'retrained_graph.pb'

    if os.path.isfile(graph_file):
        result = time.ctime(os.path.getmtime(graph_file))

    return result

def is_trainable(labels):
    result = False
    score = 0
    if len(labels) > 1:
        for label in labels:
            if label['items'] >= 1:
                score += 1
                
    if score > 1:
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
            labels = get_labels(dataset_path)

            dataset = {
                "name": dataset_name,
                "labels": labels,
                "path": dataset_path,
                "trained": is_trained(dataset_path),
                "last_trained_on": last_trained_date(dataset_path),
                "trainable": is_trainable(labels)
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
    
    def add_files(self, request, dataset_name, label_name):

        result = []
        request_json = {}
        label_dir = self.datasets_dir + \
            normalize_name(dataset_name) + '/' + 'labels/' + label_name

        make_dir(label_dir)

        # if url passed to json body
        try:
            request_json = request.json

        except Exception as e:
            print(e)

        if 'urls' in request_json.keys():
            result = save_from_urls(request_json['urls'], label_dir)

        # if file passed in body
        else:
            result = save_from_bytes(request.body, label_dir)
        
        return result
