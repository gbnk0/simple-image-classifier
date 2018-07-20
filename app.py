from sanic import Sanic
from sanic.response import json
from responses import *
import database as db

app = Sanic()

@app.post('/label')
async def route_label_picture(request):
    return json({'data': 'a smartphone'})


@app.get('/datasets')
async def route_get_datases(request):
    return json(db.get_datasets(), status=200)

@app.put('/datasets')
async def route_new_dataset(request):
    result = resp_error
    if len(request.json) > 0:
        if db.insert_dataset(request.json['name']):
            result = resp_created
        else:
            result = resp_conflict
        
    return json(result, status=201)

if __name__ == '__main__':
    db.make_dir('data/')
    db.create_tables()
    db.insert_dataset('test1')
    db.get_datasets()
    app.run(host='0.0.0.0', port=8080)
    db.close()
