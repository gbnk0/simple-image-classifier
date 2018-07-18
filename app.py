import os
import sqlite3
from sanic import Sanic
from sanic.response import json

app = Sanic()

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Created '{}' directory.".format(directory))

def create_tables():
    cursor = app.db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datasets(id INTEGER PRIMARY KEY, name TEXT,
                                path TEXT)
    ''')
    app.db.commit()

# class Datasets(object):

#     def __init__(self, *args):
 


@app.post('/label')
async def route_label_picture(request):
    return json({'data': 'a smartphone'})

@app.post('/new/dataset')
async def route_new_dataset(request):
    if len(request.json) > 0:
        d = Dataset(request.json.name)
    return json({'status': 'created'})

if __name__ == '__main__':
    make_dir('data/')
    app.db = sqlite3.connect('data/classifier.db')
    create_tables()
    app.run(host='0.0.0.0', port=8000)
    app.db.close()
