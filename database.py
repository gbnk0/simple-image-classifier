import os
import sqlite3

db = sqlite3.connect('data/classifier.db')

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Created '{}' directory.".format(directory))


def create_tables():
    c = db.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS datasets(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)
    ''')
    db.commit()


def get_datasets():
    results = []
    c = db.cursor()
    for row in c.execute('SELECT * FROM datasets ORDER BY name'):
        row = dict([row])
        results.append(row)
    return results


def insert_dataset(name):
    result = False
    c = db.cursor()
    try:
        c.execute("INSERT INTO datasets(name) VALUES ('{}')".format(name.lower()))
        db.commit()
        result = True
    except Exception as e:
        print(e)
    return result

def close():
    db.close()