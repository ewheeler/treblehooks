import json
import urlparse
import uuid
import util

class Task(object):
    def __init__(self, content_type, body):
        self.id = str(uuid.uuid4())
        if util.walks_like_json(content_type):
            data = json.loads(body)
            self.url = data.get('url')
            self.method = data.get('method', 'POST')
            self.result_callback_url = data.get('result_callback_url')
            self.params = json.dumps(data.get('params', {}))
            self.adapter_names = data.get('adapter_names')
        elif util.talks_like_form(content_type):
            data = urlparse.parse_qs(body)
            self.url = data.get('task.url',[])[0]
            self.method = data.get('task.method', ['POST'])[0]
            self.result_callback_url = data.get('task.result_callback_url'[None])[0]
            self.params = json.dumps(dict([(k,v[0]) for k,v in data.items() if not k.startswith('task.')]))
            self.adapter_names = data.get('adapter_names')
        else:
            raise NotImplementedError("content type not supported: %s" % content_type)
