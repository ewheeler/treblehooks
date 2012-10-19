import json

from gevent import wsgi
from flask import Flask, request, jsonify

from redis import Redis
from rq import Queue

from dispatcher import dispatch
from task import Task

q = Queue(connection=Redis())

app = Flask(__name__)
app.debug = True

@app.route("/queue/", methods=['GET', 'POST'])
def queue():
    content_type = request.headers.get('Content-type')
    task = Task(content_type, request.data)
    job = q.enqueue(dispatch, task)
    return jsonify({'task_id': task.id, 'job_id': job.id})

@app.route("/dhis/api/", methods=['GET', 'POST'])
def fake_dhis():
    """
    curl -H "Content-Type: application/json" -d '{"url": "http://localhost:8080/", "adapter_config": "dhis_config", "adapter": "dhis_xml", "result_callack_url": "http://localhost:8080/callback/", "params": {"week": "42", "data": [{"type": "wat", "slug": "foo", "value": "8"}], "facility": "foo"}, "countdown": "7"}' http://localhost:8080/queue/
    """
    print request.headers
    print request.data
    return jsonify({'status': 'success'})

@app.route("/foo/api/", methods=['GET', 'POST'])
def fake_foo():
    """
    curl -H "Content-Type: application/json" -d '{"url": "http://localhost:8080/", "adapter_config": foo_config", "adapter": "foo_json", "result_callback_url": "http://localhost:8080/callback/", "params": {"week": "42", "data": [{"type": "wat", "slug": "foo", "value": "8"}], "facility": "foo"}, "countdown": "7"}' http://localhost:8080/queue/
    """
    print request.headers
    print request.json
    data = request.json.get('data')
    return jsonify({'status': 'success'})

@app.route("/callback/", methods=['GET', 'POST'])
def fake_callback():
    print request.headers
    print request.data
    return jsonify({'status': 'success'})

print 'Serving on 8080...'
wsgi.WSGIServer(('', 8080), app).serve_forever()
