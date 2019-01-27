from calculator import average_features, similarity
from flask import Flask, jsonify, request
from models import Testtable, Locations
from connectors.SpotifyConnector import get_top_tracks, get_song_features
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


@app.route('/api/myrecommendations/', methods=['GET'])
def get_user_features():
    user_token = request.headers.get('user_token')
    top_track_ids = get_top_tracks(user_token)
    track_features = get_song_features(top_track_ids)
    res = session.query(Locations).all()
    result_dict = [json.dumps(res, cls=JSONSerializer) for r in res]
    similarity_scores = []
    for location in result_dict:
        similarity_scores.append({'score': similarity(track_features, location),
                                  'longititude': location.longitude, 'latitude': location.latitude})

    return jsonify(result=similarity_scores)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
