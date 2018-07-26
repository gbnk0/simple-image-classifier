import requests

class SimpleClassifier(object):

    def __init__(self, **kwargs):
        self.host = kwargs.get('host', "localhost")
        self.port = kwargs.get('port', 8080)
        self.proto = kwargs.get('proto', "http")
        self.uri = "{}://{}:{}".format(self.proto, self.host, self.port)
        self.datasets = self.init_datasets()

    def init_datasets(self):
        return SimpleClassifier.Datasets(self)
    
    def json_query(self, path, method, **kwargs):
        r = requests.request(method, self.uri + path, json=kwargs)
        print(r.text)
        return r.json()
    
    class Datasets(object):

        def __init__(self, classifier):
            self.classifier = classifier
        
        def get(self, dataset=None):
            path = '/datasets'
            if dataset:
                path = path + '/' + dataset
            result = self.classifier.json_query(path, 'GET')
            return result
        
        def create(self, name):
            result = self.classifier.json_query('/datasets', 'PUT', name=name)
            return result

        def addPicture(self, dataset, **kwargs):
            result = {}
            urls = kwargs.get('urls', [])
            label = kwargs.get('label')

            path = '/datasets/' + dataset + '/' + label

            if not isinstance(urls, list):
                if isinstance(urls, str):
                    urls = [urls]

            result = self.classifier.json_query(path, 'PUT', urls=urls)

            return result

        def train(self, dataset, **kwargs):
            path = '/datasets/' + dataset + '/train'
            result = self.classifier.json_query(path, 'POST', **kwargs)
            return result
        
        def classify(self, dataset, **kwargs):
            path = '/datasets/' + dataset + '/label'
            result = self.classifier.json_query(path, 'POST', **kwargs)
            return result
