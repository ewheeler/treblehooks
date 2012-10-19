import json
import requests

import util
import adapters

class TaskFailure(Exception):
    pass

def dispatch(task):
    try:
        print('start:%s\n' % task.id)
        
        if task.url.startswith('http'):
            headers = {"User-Agent": "RSMSAggregatesWebService/0.1", "X-Task": task.id, "Content-type": "application/json"}
            if task.adapter is not None:
                if hasattr(adapters, task.adapter):
                    # if caller specified an adapter, run adapter
                    target, adapter_headers, payload = getattr(adapters, task.adapter)(task.params, task.adapter_config)
                    # update task based on adapter output
                    task.url = target
                    headers.update(adapter_headers)
                    task.params = payload

            resp = requests.request(task.method, task.url, headers=headers, data=task.params)
            content = resp.content
            if task.result_callback_url:
                # if caller specified a result_callback_url
                result_content_type = resp.headers.get('content-type')
                result_data = {}
                if content is not None:
                    if resp.json:
                        result_data = resp.json
                    elif util.talks_like_form(result_content_type):
                        result_data = dict([(k,v[0]) for k,v in urlparse.parse_qs(content).items() ])
                    else:
                        try:
                            result_data = json.loads(content)
                        except Exception, e:
                            try:
                                result_data = dict([(k,v[0]) for k,v in urlparse.parse_qs(content).items() ])
                            except Exception, e:
                                pass
                if not result_data:
                    result_data = {}
                result_data.update({'status': resp.status_code, 'reason': resp.reason, 'content-type': result_content_type})
                callback_resp = requests.request('POST', task.result_callback_url, data=json.dumps(result_data))
        print('success:%s\n' % task.id)
        return True
    except (TaskFailure), e:
        print('failure:%s:%s\n' % (task.id, str(e)))
        return False

