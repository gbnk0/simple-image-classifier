# simple-image-classifier
Simple image classifier microservice using tensorflow

#### PREREQUISITES FOR LOCAL RUN
- A linux system
- python >= 3.5

#### QUICKSTART GUIDE ==
Go to the app folder:
```
cd app/
pip3 install -r requirements.txt
python3 app.py
```

It will listen on localhost:8080

#### POPULATING DATASET

When you successfully created a dataset using the /datasets endpoint:
One method for populating the new dataset is to copy all your categories folders (dog, cat, fish, people) to the data/{datasetName}/labels/ folder.


#### POSTMAN DOC:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/3045659/RWMHM7ir)
