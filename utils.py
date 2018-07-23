import os
import sys
import re
import uuid
import requests
import threading
import subprocess
import filetype
import retrain

def is_jpeg(file):
    result = False
    file_type = filetype.guess(file).mime.lower().split('/')[1]

    if file_type in ['jpg', 'jpeg']:
        result = True

    return result

def save_from_bytes(file_bytes, dest_file):
    result = False
    if is_jpeg(file_bytes):
        with open(dest_file, 'wb') as file:
            file.write(file_bytes)
            result = True
    return result

def save_from_url(url, dest_file):
    result = False

    with open(dest_file, "wb") as f:
        response = requests.get(url)

        file = response.content
        if is_jpeg(file):
            f.write(file)
            result = True

    return result

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

def train(dataset_path, training_steps):
    bottleneck_dir = dataset_path + 'bottlenecks'
    labels_path = dataset_path + "labels/"
    output_graph = dataset_path + "retrained_graph.pb"
    output_labels = dataset_path + "retrained_labels.txt"

    retrain.run(bottleneck_dir=bottleneck_dir, 
                how_many_training_steps=training_steps,
                image_dir=labels_path, output_graph=output_graph,
                output_labels=output_labels)

def classify(dataset_path, request):
    filename = make_uuid() + '.jpg'
    filepath = dataset_path + '/' + filename

    # if url passed to json body
    try:
        request_json = request.json
    except:
        request_json = {}

    if 'url' in request_json.keys():
        save_from_url(request_json['url'], filepath)
    # if file passed in body
    else:
        save_from_bytes(request.body, filepath)
    # ADD sys.executable for python bin

    results = []
    train_cmd = "{0} label.py "\
                "--output_layer=final_result "\
                "--input_layer=Placeholder "\
                "--graph={1}retrained_graph.pb "\
                "--labels={1}retrained_labels.txt "\
                "--image {2}".format(sys.executable, dataset_path, filepath)
    print(train_cmd)
    # very dirty part
    result = str(subprocess.check_output(train_cmd, shell=True))
    print(result)
    labels = result.split('### LABELS:')[1]
    labels = labels.split('LABEL: ')
    for l in labels:
        if len(l) > 2:
            accuracy = re.findall("\d+\.\d+", l)[0]
            accuracy = float(accuracy) * 100
            label = l.rstrip().split(' ->')[0]
            label = label.replace(' [', '').replace(']', '')
            data = {
                "label": label,
                "accuracy": accuracy
            }
            results.append(data)
    print(results)
    os.remove(filepath)
    return results


class Run(threading.Thread):

  def __init__(self, queue):
    threading.Thread.__init__(self)
    self.queue = queue

  def run(self):
    while True:
        task = self.queue.get()
        if task['action'] == 'train':
            dataset_path = task['dataset']['path']
            training_steps = int(task['training_steps'])
            train(dataset_path, training_steps)
        self.queue.task_done()
