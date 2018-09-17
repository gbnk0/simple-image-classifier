import os
import re
import uuid
import shutil
import requests
import threading
import filetype
import retrain
from label import Classify
from pathlib import Path
import hashlib

def is_jpeg(file):
    result = False
    file_type = filetype.guess(file).mime.lower().split('/')[1]

    if file_type in ['jpg', 'jpeg']:
        result = True

    return result

def save_from_bytes(file_bytes, label_dir, hashs):
    result = []
    new_hashs = []

    filename = make_uuid() + '.jpg'
    filepath = label_dir + '/' + filename

    saved_file, new_hash = save_file(file_bytes, filepath, hashs)
    if len(saved_file) > 0:
        result.append(saved_file)
        new_hashs.append(new_hash)

    return result, new_hashs

def save_from_urls(urls, dest_dir, hashs):
    result = []
    new_hashs = []
    for url in urls:
        filename = make_uuid() + '.jpg'
        filepath = dest_dir + '/' + filename
        response = requests.get(url)
        file_bytes = response.content

        saved_file, new_hash = save_file(file_bytes, filepath, hashs)
        if len(saved_file) > 0:
            result.append(saved_file)
            new_hashs.append(new_hash)


    return result, new_hashs

def save_file(file_bytes, filepath, hashs=[]):
    result = ""
    img_hash = hashlib.md5(file_bytes).hexdigest()
    if not img_hash in hashs:
        if is_jpeg(file_bytes):
            with open(filepath, "wb") as file:
                file.write(file_bytes)
                result = filepath
    else:
        print('Image hash already exists in database.')

    return result, img_hash

def make_dir(directory):
    result = False
    if not os.path.exists(directory):
        os.makedirs(directory)
        result = True
    return result

def make_uuid():
    result = uuid.uuid4()
    return str(result)

def normalize_name(s):
    s = s.lower()
    s = re.sub(r"\s+", '_', s)
    return s

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def delete_dir(path) :
    return shutil.rmtree(path, ignore_errors=True)

def classify(dataset, bundle, request):
    labels = []
    dataset_path = dataset['path']
    request_json = {}

    if dataset['trained'] == True:
        # if url passed to json body
        try:
            request_json = request.json

        except Exception as e:
            print(e)

        if 'url' in request_json.keys():
            url = request_json['url']
            filepath, _ = save_from_urls([url], dataset_path, [])
        # if file passed in body
        else:
            filepath, _ = save_from_bytes(request.body, dataset_path, [])
        
        if len(filepath) > 0:
            filepath = filepath[0]

        labels_path = dataset_path + "retrained_labels.txt"

        cl = bundle[dataset['name']]
        labels = cl.run(filename=filepath,
                        output_layer="final_result",
                        input_layer="Placeholder",
                        labels=labels_path)

        remove_file(filepath)

    return list(labels)

# Tensorflow training function
def train(dataset_path, training_steps):
    bottleneck_dir = dataset_path + 'bottlenecks'
    labels_path = dataset_path + "labels/"
    output_graph = dataset_path + "retrained_graph.pb"
    output_labels = dataset_path + "retrained_labels.txt"

    return retrain.run(bottleneck_dir=bottleneck_dir,
                how_many_training_steps=training_steps,
                image_dir=labels_path, output_graph=output_graph,
                output_labels=output_labels)

class TrainWorker(object):

    def __init__(self, dataset_path, training_steps):
        self.dataset_path = dataset_path
        self.training_steps = training_steps

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):        
        results = train(self.dataset_path, self.training_steps)
        return results

    
def get_version():
    version = "unknown"
    version_file = 'version.txt'
    if os.path.isfile(version_file):
        with open(version_file, 'r') as f:
            version = f.read().strip()
    return version
