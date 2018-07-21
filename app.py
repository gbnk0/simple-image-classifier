import os
from sanic import Sanic
from sanic.response import json
from responses import *
from datasets import Datasets
from utils import make_dir, normalize_name

app = Sanic()

data_dir = 'data/'
datasets_dir = data_dir + 'datasets/'

datasets = Datasets(datasets_dir)

@app.route('/datasets', methods=['GET'])
async def route_get_datases(request):
    return json(datasets.get(), status=200)


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
    result = resp_error()
    file_added = datasets.add_file(request, dataset_name, label_name)

    if file_added:
        result = resp_created()

    return json(result, status=201)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
