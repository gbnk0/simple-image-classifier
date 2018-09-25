import os
import time
import json
from urllib.parse import unquote
from utils import make_dir, normalize_name, save_from_urls, save_from_bytes, delete_dir

def is_trained(dataset_path):
    result = False
    if os.path.isfile(dataset_path + 'retrained_labels.txt'):
        if os.path.isfile(dataset_path + 'retrained_graph.pb'):
            result = True
    return result

def get_labels(dataset_path):
    labels = []
    labels_path = dataset_path + 'labels'
    if os.path.isdir(labels_path):
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
            if label['items'] >= 10:
                score += 1

    if score > 1:
        result = True
    
    return result

def get_hashs(dataset_dir, label_name):
    hashs = []
    hashs_file = dataset_dir + '/' + label_name + '.json'

    if os.path.isfile(hashs_file):
        with open(hashs_file, 'r') as f:
            hashs = json.load(f)["hashs"]
    else:
        with open(hashs_file, 'w') as f:
            f.write(json.dumps({"hashs":[]}))
    return hashs


def update_hashs(dataset_dir, label_name, old_hashs, new_hashs):
    hashs_file = dataset_dir + '/' + label_name + '.json'

    if len(new_hashs) > 0:
        updated_hashs = list(old_hashs)
        updated_hashs.extend(h for h in new_hashs if h not in old_hashs)

        with open(hashs_file, 'w') as f:
            f.write(json.dumps({"hashs":updated_hashs}))

    return True

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
    
    def delete(self, name):
        name = normalize_name(name)
        dataset_path = self.datasets_dir + name
        delete_dir(dataset_path)
        return
    
    def add_files(self, request, dataset_name, label_name):

        result = {
            "new_files": []
        }
        request_json = {}

        # if url passed to json body
        try:
            if isinstance(request.json, dict):
                request_json = request.json

        except Exception as e:
            print(e)

        dataset_path = self.datasets_dir + normalize_name(dataset_name)
        label_dir = dataset_path + '/' + 'labels/' + label_name
        # decode url format
        label_dir = unquote(label_dir)
        # make label dir if not exists
        make_dir(label_dir)

        new_files = []
        new_hashs = []
        hashs = get_hashs(dataset_path, label_name)

        if 'urls' in request_json.keys():
            new_files, new_hashs = save_from_urls(request_json['urls'], label_dir, hashs)
        # if file passed in body
        else:
            if len(request.body) > 32:
                new_files, new_hashs = save_from_bytes(request.body, label_dir, hashs)

        update_hashs(dataset_path, label_name, hashs, new_hashs)

        
        result['new_files'] = new_files

        return result
