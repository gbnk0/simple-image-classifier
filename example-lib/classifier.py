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
        result = {}
        print(kwargs)
        r = requests.request(method, self.uri + path, json=kwargs)
        return r.json()
    
    class Datasets(object):

        def __init__(self, classifier):
            self.classifier = classifier
        
        def getAll(self):
            result = self.classifier.json_query('/datasets', 'GET')
            return result
        
        def get(self, dataset_name):
            path = '/datasets/' + dataset_name
            result = self.classifier.json_query(path, 'GET')
            return result
        
        def create(self, name):
            result = self.classifier.json_query('/datasets', 'PUT', name=name)
            return result
        
        def train(self, dataset_name, **kwargs):
            path = '/datasets/' + dataset_name + '/train'
            result = self.classifier.json_query(path, 'POST', **kwargs)
            return result


if __name__ == "__main__":
    s = SimpleClassifier(host='localhost', port=8080, proto="http")
    print("Classifier URI: ", s.uri)
    print("Get all available datasets: ", s.datasets.getAll())
    print("Create one dataset: ", s.datasets.create('animals'))
    # Add pictures
    print("Get one dataset: ", s.datasets.get('animals'))
    print("Launching dataset training: ", s.datasets.train('animals', training_steps=50))



