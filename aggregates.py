import json

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
    curl -H "Content-Type: application/json" -d '{"adapter_config": "dhis_config","result_callback_url": "http://localhost:8080/callback/", "params": {"week": "42", "data": [{"type": "wat", "slug": "foo", "value": "8"}], "facility": "foo"}}' http://localhost:8080/queue/
    curl -H "Content-Type: application/json" -d '{"adapter_config": "my_dhis_config", "result_callback_url": "http://localhost:8080/callback/", "params": {"week": "42", "data": [{"type": "wat", "slug": "foo", "value": "8"}], "facility": "foo"}}' http://localhost:8080/queue/
    """
    print request.headers
    print request.data
    return jsonify({'status': 'success'})

@app.route("/foo/api/", methods=['GET', 'POST'])
def fake_foo():
    """
    curl -H "Content-Type: application/json" -d '{"adapter_config": "foo_config", "result_callback_url": "http://localhost:8080/callback/", "params": {"week": "42", "data": [{"type": "wat", "slug": "foo", "value": "8"}], "facility": "foo"}}' http://localhost:8080/queue/
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

if __name__ == '__main__':
    print 'Serving on 8080...'
    app.run(host='0.0.0.0', port=8080)
