import json
import requests

import util
import adapter

class TaskFailure(Exception):
    pass

def dispatch(task):
    try:
        print('start:%s\n' % task.id)
        
        if task.url.startswith('http'):
            headers = {"User-Agent": "RSMSAggregatesWebService/0.1", "X-Task": task.id, "Content-type": "application/json"}
            if task.adapter_config is not None:
                target, adapter_headers, payload = adapter.Adapter(task.params, task.adapter_config).execute()
                task.url = target
                headers.update(adapter_headers)
                task.params = payload

            resp = requests.request(task.method, task.url, headers=headers, data=task.params)
            if task.result_callback_url:
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
                            result_data = json.loads(resp.content)
                        except Exception, e:
                            try:
                                result_data = dict([(k,v[0]) for k,v in urlparse.parse_qs(resp.content).items() ])
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

