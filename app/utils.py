import os
import re
import uuid
import requests
import threading
import filetype
import retrain
import label
from pathlib import Path

def is_jpeg(file):
    result = False
    file_type = filetype.guess(file).mime.lower().split('/')[1]

    if file_type in ['jpg', 'jpeg']:
        result = True

    return result

def save_from_bytes(file_bytes, label_dir):
    result = []

    filename = make_uuid() + '.jpg'
    filepath = label_dir + '/' + filename
    
    if is_jpeg(file_bytes):
        with open(filepath, 'wb') as file:
            file.write(file_bytes)
            result.append(filepath)

    return result

def save_from_urls(urls, label_dir):
    saved_files = []

    for url in urls:
        filename = make_uuid() + '.jpg'
        filepath = label_dir + '/' + filename
        
        with open(filepath, "wb") as f:
            
            response = requests.get(url)
            file = response.content

            if is_jpeg(file):
                f.write(file)
                saved_files.append(filepath)

    return saved_files

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


def classify(dataset_path, request):
    request_json = {}
    filename = make_uuid() + '.jpg'
    filepath = dataset_path + '/' + filename

    # if url passed to json body
    try:
        request_json = request.json

    except Exception as e:
        print(e)

    if 'url' in request_json.keys():
        save_from_urls([request_json['url']], filepath)
    # if file passed in body
    else:
        save_from_bytes(request.body, filepath)

    graph_path = dataset_path + "retrained_graph.pb"
    labels_path = dataset_path + "retrained_labels.txt"
    labels = label.run(filename=filepath,
                       output_layer="final_result",
                       input_layer="Placeholder",
                       graph=graph_path,
                       labels=labels_path)

    return list(labels)

def remove_files(path, files):
    for p in Path(path).glob(files):
        p.unlink()

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
        print('WORKER LAUNCHED')
        
        try:
            train(self.dataset_path, self.training_steps)
            
        except Exception as e:
            print(e)

def configure_app(app):
    app.config.debug = True
    app.config.port = 8080
    app.config.host = "0.0.0.0"
    app.config.LOGO = None
    