from sanic import Sanic
from sanic.response import json
from responses import *
from datasets import Datasets
from queue import Queue
from utils import Worker, classify, configure_app

app = Sanic()
configure_app(app)

queue = Queue()

data_dir = 'data/'
datasets_dir = data_dir + 'datasets/'

datasets = Datasets(datasets_dir)

@app.route('/datasets', methods=['GET'])
async def route_get_datasets(request):
    return json(datasets.get(), status=200)


@app.route('/datasets/<dataset_name>', methods=['GET'])
async def route_get_one_dataset(request, dataset_name):
    return json(datasets.get(name=dataset_name), status=200)

@app.route('/datasets', methods=['PUT'])
async def route_new_dataset(request):
    result = resp_error()
    if len(request.json) > 0:
        dataset_name = request.json['name']
        
        if datasets.create(dataset_name):
            result = resp_created()

            result['data'] = {
                "name": dataset_name
            }

        else:
            result = resp_conflict()
        
    return json(result, status=201)


@app.route('/datasets/<dataset_name>/<label_name>', methods=['PUT'])
async def route_new_file(request, dataset_name, label_name):
    result = json(resp_error(), status=500)
    file_added = datasets.add_file(request, dataset_name, label_name)

    if file_added:
        result = json(resp_created(), status=201)

    return result


@app.route('/datasets/<dataset_name>/train', methods=['POST'])
async def route_train_dataset(request, dataset_name):
    result = resp_success()
    request_json = request.json

    dataset = datasets.get(name=dataset_name)
    
    train_task = {
        "action": "train",
        "dataset": dataset,
        "training_steps": request_json.get('training_steps', 50)
    }

    queue.put(train_task)
    result['data'] = {}
    result['data']['task'] = train_task

    return json(result, status=201)


@app.route('/datasets/<dataset_name>/label', methods=['POST'])
async def route_label_item(request, dataset_name):
    result = resp_success()
    dataset = datasets.get(name=dataset_name)
    labels = classify(dataset['path'], request)
    result['data'] = labels

    return json(result, status=201)
    

@app.route('/tasks', methods=['GET'])
async def route_get_tasks(request):
    result = {
        "remaining": queue.qsize()
    }
    return json(result, status=200)


p = Worker(queue)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

