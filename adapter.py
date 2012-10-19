from lxml import etree
import uritemplate
import pystache

import datetime
import base64
import json

import dispatcher
import config

def reconcile_token(adapter, token):
    if adapter in ['DHIS_CONFIG']:
        TOKEN_MAP = {'foo': 'bar', 'wat': 'who'}
    else:
        TOKEN_MAP = {'foo': 'FOO', 'wat': 'WAT'}
    # caller should watch for KeyError!
    return TOKEN_MAP[token]

class Adapter(object):
    def __init__(self, params, adapter_config):
        if adapter_config is not None:
            if hasattr(config, adapter_config.upper()):
                self.config = getattr(config, adapter_config.upper())
        else:
            raise dispatcher.TaskFailure('No adapter configuration named: %s' % adapter_config)
        self.adapter = adapter_config.upper()
        self.uri = uritemplate.expand(config.URI_TEMPLATE, self.config)
        self.data = self._reconcile_tokens(params)
        self.payload = self._build_payload()

    def _reconcile_tokens(self, params):
        data = json.loads(params)
        if 'body_reconcile_tokens' in self.config:
            for token in self.config['body_reconcile_tokens']:
                data[token] = reconcile_token(self.adapter, data[token])
        if 'data_item_reconcile_tokens' in self.config:
            for datum in data.get('data'):
                for token in self.config['data_item_reconcile_tokens']:
                    if token in datum:
                        datum[token] = reconcile_token(self.adapter, datum[token])
        data['report_date'] = datetime.datetime.now().strftime(self.config['datetime_format'])
        return data

    def _build_payload(self):
        renderer = pystache.Renderer(escape=lambda u: u)
        data_items = []
        if 'data_item_template' in self.config:
            for data_dict in self.data['data']:
                data_items.append(renderer.render(self.config['data_item_template'],\
                        {'slug': data_dict['slug'], 'type': data_dict['type'],\
                        'value': data_dict['value']}))

        return renderer.render(self.config['body_template'], {'week': self.data['week'],\
                'facility': self.data['facility'], 'data_items': ''.join(data_items),\
                'report_date': self.data['report_date']})

    def _execute_json(self):
        # eval rendered template into a dict
        json_payload_dict = eval(self.payload)
        self.payload = json.dumps(json_payload_dict)
        headers = {
            "Content-type": "application/json",
        }
        return self.uri, headers, self.payload

    def _execute_xml(self):
        auth_token = base64.b64encode("%s:%s" %\
                (self.config['user'], self.config['pass']))
        headers = {
            "Content-type": "application/xml",
            "Authorization": "Basic %s" % (auth_token)
        }
        return self.uri, headers, self.payload

    def execute(self):
        if self.config['template_type'] == 'json':
            return self._execute_json()
        if self.config['template_type'] == 'xml':
            return self._execute_xml()
