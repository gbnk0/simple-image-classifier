import os
import re
import uuid
import requests
import threading
import subprocess
import filetype

def is_jpeg(file):
    result = False
    file_type = filetype.guess(file).mime.lower().split('/')[1]

    if file_type in ['jpg', 'jpeg']:
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


def syscmd(cmd, encoding=''):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
              close_fds=True)
    p.wait()
    output = p.stdout.read()
    if len(output) > 1:
        return output
    return p.returncode


def train(dataset_path, training_steps):
    bottleneck_dir = dataset_path + 'bottlenecks'
    train_cmd = "python3.6 retrain.py "\
                "--bottleneck_dir={0} "\
                "--how_many_training_steps={1} "\
                "--output_graph={2}retrained_graph.pb "\
                "--output_labels={2}retrained_labels.txt "\
                "--image_dir {2}labels/".format(bottleneck_dir, training_steps, dataset_path)
    print(train_cmd)
    print(subprocess.check_output(train_cmd, shell=True))


class Run(threading.Thread):

  def __init__(self, queue):
    threading.Thread.__init__(self)
    self.queue = queue

  def run(self):
    while True:
        task = self.queue.get()
        if task['action'] == 'train':
            print(task)
            dataset_path = task['dataset']['path']
            training_steps = int(task['training_steps'])
            train(dataset_path, training_steps)
        self.queue.task_done()
