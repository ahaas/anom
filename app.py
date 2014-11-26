from flask import Flask, render_template, url_for, jsonify
import json

# sMAP dependencies
from smap.archiver.client import SmapClient
import time
import datetime
import pandas as pd

import pprint
pp = pprint.PrettyPrinter(indent=2)

app = Flask(__name__)

client = SmapClient('http://new.openbms.org/backend')

def get_data(client, query, start, end):
    """ Returns numpy data for queried uuids """
    uuids = [x['uuid'] for x in client.query(query)]
    data = dict(zip(uuids, client.data_uuid(uuids, start, end, cache=False)))
    pp.pprint(data)
    return data

def prepare_ts_for_graph(numpy_array):
    out = numpy_array.tolist()
    out = [{'x': v[0], 'y': v[1]} for idx, v in enumerate(out) if not idx%1000]
    return out

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    now = int(time.time())
    q_get_keti = 'select uuid where Metadata/SourceName ="Nano Lab KETI Motes" and Path like "%illumination"'
    data1 = get_data(client, q_get_keti, now-60*60*24*60, now) # TODO: unhardcode time
    q_get_keti = 'select uuid where Metadata/SourceName ="Nano Lab KETI Motes" and Path like "%co2"'
    data2 = get_data(client, q_get_keti, now-60*60*24*60, now) # TODO: unhardcode time
    data = dict(data1.items() + data2.items())
    out = jsonify(
        {
            k: {'key': k,
                'values': prepare_ts_for_graph(v)}
            for k, v in data.items()
        }
    )
    pp.pprint(out)
    return out

if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)
