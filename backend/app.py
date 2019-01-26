from flask import Flask
from models import Testtable
from db import session
from serializer import JSONSerializer
import json
import pdb
app = Flask(__name__)


@app.route('/')
def hello():

    my_test = Testtable("wew")
    session.add(my_test)
    res = session.query(Testtable).all()
    for r in res:
        print(json.dumps(r, cls=JSONSerializer))

    # return res


if __name__ == '__main__':
    app.run()
