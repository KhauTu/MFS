import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds215019.mlab.com:15019/mfs

host = "ds215019.mlab.com"
port = 15019
db_name = "mfs"
user_name = "admin"
password = "admin"

def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]

def item2json(item):
    import json
    return json.loads(item.to_json())
