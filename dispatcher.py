import json
import requests

import util
import adapter

class TaskFailure(Exception):
    pass

def _adapt_task(task, adapter_name):
    target, adapter_headers, payload = adapter.Adapter(task.params, adapter_name).execute()
    task.url = target
    task.headers.update(adapter_headers)
    task.payload = payload
    return task

def dispatch(task):
    try:
        print('start:%s\n' % task.id)
        
        task.headers = {"User-Agent": "WebServiceMediator/0.1", "X-Task": task.id, "Content-type": "application/json"}
        if task.adapter_names is not None:
            adapter_names = task.adapter_names.split(',')
            for adapter_name in adapter_names:
                task = _adapt_task(task, adapter_name)

                response = requests.request(task.method, task.url, headers=task.headers, data=task.payload)
                if task.result_callback_url:
                    _call_callback(task, adapter_name, response)

        print('success:%s\n' % task.id)
        return True
    except (TaskFailure), e:
        print('failure:%s:%s\n' % (task.id, str(e)))
        return False

def _call_callback(task, adapter_name, resp):
    try:
        # if caller specified a result_callback_url
        result_content_type = resp.headers.get('content-type')
        result_data = {}
        if resp.content is not None:
            if resp.json:
                result_data = resp.json
            elif util.talks_like_form(result_content_type):
                result_data = dict([(k,v[0]) for k,v in urlparse.parse_qs(resp.content).items() ])
            else:
                try:
                    result_data = dict([(k,v[0]) for k,v in urlparse.parse_qs(resp.content).items() ])
                except Exception, e:
                    pass
        if not result_data:
            result_data = {}
        result_data.update({'adapter_name': adapter_name,\
                'task_id': task.id,
                'status': resp.status_code, 'reason': resp.reason,\
                'content-type': result_content_type})
        callback_resp = requests.request('POST',\
                task.result_callback_url, data=json.dumps(result_data))
    except Exception, e:
        print e
