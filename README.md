# simple-image-classifier
Simple image classifier microservice using tensorflow

![pipeline status](https://travis-ci.org/gbnk0/simple-image-classifier.svg?branch=master)
![python_version](https://img.shields.io/badge/python-3.5%2C3.6-blue.svg)


#### PREREQUISITES FOR LOCAL RUN
- A linux system
- python >= 3.5

#### QUICKSTART GUIDE

##### RUN WITH DOCKER
``` 
docker run -p8080:8080 gbnk0/simple-image-classifier:latest
```

##### 
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
