from classifier import SimpleClassifier

if __name__ == "__main__":
    s = SimpleClassifier(host='localhost', port=8080, proto="http")
    print("Classifier URI: ", s.uri)
    print("Get all available datasets: ", s.datasets.getAll())
    print("Create one dataset: ", s.datasets.create('animals'))
    # Add pictures
    print("Get one dataset: ", s.datasets.get('animals'))
    print("Launching dataset training: ",
          s.datasets.train('animals', training_steps=50))
