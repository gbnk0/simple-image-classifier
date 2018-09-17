from sanic import Sanic
from sanic.response import json
from responses import resp
from config import datasets, configure_app, datasets_bundle, load_dataset_graphs
from utils import TrainWorker, classify, get_version

app = Sanic()
configure_app(app)

@app.route('/datasets', methods=['GET'])
async def route_get_datasets(request):
    return json(datasets.get(), status=200)

@app.route('/datasets/<dataset_name>', methods=['GET'])
async def route_get_one_dataset(request, dataset_name):
    return json(datasets.get(name=dataset_name), status=200)

@app.route('/datasets/<dataset_name>', methods=['DELETE'])
async def route_delete_one_dataset(request, dataset_name):
    result = resp('success')
    datasets.delete(dataset_name)
    return json(result, status=200)

@app.route('/datasets', methods=['PUT'])
async def route_new_dataset(request):
    result = resp('error')
    if len(request.json) > 0:
        dataset_name = request.json['name']
        
        if datasets.create(dataset_name):
            result = resp('created')

            result['data'] = {
                "name": dataset_name
            }

        else:
            result = resp('conflict')
        
    return json(result, status=201)

@app.route('/datasets/<dataset_name>/<label_name>', methods=['PUT'])
async def route_new_file(request, dataset_name, label_name):
    result = json(resp('error'), status=500)
    files_added = datasets.add_files(request, dataset_name, label_name)
    new_files = files_added['new_files']

    if len(new_files) > 0:
        result_data = resp('created')
        result_data['data'] = files_added
        result = json(result_data, status=201)
    else:
        result_data = resp('error')
        result_data['reason'] = "Maybe you forgot to specify some files to upload, or the files are already present in the label"
        result = json(result_data, status=200)

    return result


@app.route('/datasets/<dataset_name>/train', methods=['POST'])
async def route_train_dataset(request, dataset_name):
    result = resp('error')
    result['data'] = {}

    request_json = request.json

    dataset = datasets.get(name=dataset_name)
    training_steps = request_json.get('training_steps', 50)

    train_task = {
        "action": "train",
        "dataset": dataset,
        "training_steps": training_steps
    }
    if dataset['trainable'] == True:
        TrainWorker(dataset['path'], training_steps)
        result = resp('success')
        result['data'] = {}
        result['data']['task'] = train_task
    else:
        result['reason'] =  "This dataset is not trainable"

    return json(result, status=200)


@app.route('/datasets/<dataset_name>/label', methods=['POST'])
async def route_label_item(request, dataset_name):
    result = resp('success')
    dataset = datasets.get(name=dataset_name)
    labels = classify(dataset, datasets_bundle, request)
    if len(labels) > 0:
        result['data'] = labels
    else:
        result = resp('error')
        result['reason'] = "Maybe you have to train this dataset first."

    return json(result, status=201)

@app.route('/version')
async def route_get_version(request):
    version = get_version()
    result = {
        "version": version
    }
    return json(result, status=200)

load_dataset_graphs()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

