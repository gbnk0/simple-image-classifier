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
    c = app.db.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS datasets(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)
    ''')
    app.db.commit()

def get_datasets():
    c = app.db.cursor()
    for row in c.execute('SELECT * FROM datasets ORDER BY name'):
            print(row)

def insert_dataset(name):
    result = False
    c = app.db.cursor()
    try:
        c.execute("INSERT INTO datasets(name) VALUES ('{}')".format(name))
        app.db.commit()
        result = True
    except Exception as e:
        print(e)
    return result


@app.post('/label')
async def route_label_picture(request):
    return json({'data': 'a smartphone'})

@app.put('/dataset')
async def route_new_dataset(request):
    # if len(request.json) > 0:
        # d = insert_dataset(request.json.name)
    return json({'status': 'created'})

if __name__ == '__main__':
    make_dir('data/')
    app.db = sqlite3.connect('data/classifier.db')
    create_tables()
    insert_dataset('test1')
    get_datasets()
    app.run(host='0.0.0.0', port=8080)
    app.db.close()
