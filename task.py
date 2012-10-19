import json
import urlparse
import uuid
import util

class Task(object):
    def __init__(self, content_type, body):
        self.id = str(uuid.uuid4())
        if util.walks_like_json(content_type):
            data = json.loads(body)
            self.url = data['url']
            self.method = data.get('method', 'POST')
            self.result_callback_url = data.get('result_callback_url')
            self.params = json.dumps(data.get('params', {}))
            self.adapter = data.get('adapter')
            self.adapter_config = data.get('adapter_config')
        elif util.talks_like_form(content_type):
            data = urlparse.parse_qs(body)
            self.url = data['task.url'][0]
            self.method = data.get('task.method', ['POST'])[0]
            self.result_callback_url = data.get('task.result_callback_url'[None])[0]
            self.params = json.dumps(dict([(k,v[0]) for k,v in data.items() if not k.startswith('task.')]))
            self.adapter = data.get('adapter')
            self.adapter_config = data.get('adapter_config')
        else:
            raise NotImplementedError("content type not supported: %s" % content_type)
