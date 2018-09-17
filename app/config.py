from datasets import Datasets
from label import Classify

data_dir = 'data/'
datasets_dir = data_dir + 'datasets/'

datasets = Datasets(datasets_dir)

def configure_app(app):
    app.config.debug = True
    app.config.port = 8080
    app.config.host = "0.0.0.0"
    app.config.LOGO = None

global datasets_bundle
datasets_bundle = {}

def load_dataset_graphs():
    for dataset in datasets.get():
        dataset_name = dataset['name']
        dataset_path = dataset['path']

        graph_path = dataset_path + "retrained_graph.pb"
        datasets_bundle[dataset_name] = Classify(graph=graph_path)
    print("-> Loaded {} datasets.".format(len(datasets_bundle)))


