from datasets import Datasets

data_dir = 'data/'
datasets_dir = data_dir + 'datasets/'

datasets = Datasets(datasets_dir)

def configure_app(app):
    app.config.debug = True
    app.config.port = 8080
    app.config.host = "0.0.0.0"
    app.config.LOGO = None
