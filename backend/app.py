from flask import Flask, jsonify
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
    session.commit()

    res = session.query(Testtable).filter_by(name='wew').all()
    serialized = [json.dumps(r, cls=JSONSerializer) for r in res]

    return jsonify(result=serialized)


if __name__ == '__main__':
    app.run()
