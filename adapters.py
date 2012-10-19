from lxml import etree
import uritemplate
import pystache

import datetime
import base64
import json

import dispatcher
from config import *

def _get_dhis_element_name_for(token):
    TOKEN_MAP = {'foo': 'bar', 'wat': 'who'}
    # caller should watch for KeyError!
    return TOKEN_MAP[token]

def _build_dhis_xml_payload(adapter_config, week, facility, data_dicts):
    # attributes for the root xml element
    """
    dataValueSetAttributes = {\
        "xmlns": "http://dhis2.org/schema/dxf/2.0",
        "period": week,
        "completeDate": datetime.datetime.now().strftime('%F'),
        "orgUnit": _get_dhis_element_name_for(facility),
    }
    # create root xml element
    dataValueSet = etree.Element("dataValueSet", **dataValueSetAttributes)
    for datum in data_dicts:
        # attributes for child xml element
        dataValueAttributes = {\
            "dataElement": _get_dhis_element_name_for(datum['slug']),
            "categoryOptionCombo": _get_dhis_element_name_for(datum['type']),
            "value": datum['value']
        }
        # create child xml element
        dataValue = etree.Element("dataValue", **dataValueAttributes)
        # append to root xml element
        dataValueSet.append(dataValue)
    return dataValueSet
    """
    renderer = pystache.Renderer(escape=lambda u: u)
    data_items = []
    if 'data_item_template' in adapter_config:
        for data_dict in data_dicts:
            data_items.append(renderer.render(adapter_config['data_item_template'],\
                    {'slug': _get_dhis_element_name_for(data_dict['slug']),\
                    'type': _get_dhis_element_name_for(data_dict['type']),\
                    'value': data_dict['value']}))

    return renderer.render(adapter_config['body_template'], {'week': week,\
            'facility': _get_dhis_element_name_for(facility), 'data_items': '\n'.join(data_items),\
            'report_date': datetime.datetime.now().strftime('%F')})


def _build_foo_json_payload(adapter_config, week, facility, data_dicts):
    renderer = pystache.Renderer(escape=lambda u: u)
    data_items = []
    if 'data_item_template' in adapter_config:
        for data_dict in data_dicts:
            data_items.append(renderer.render(adapter_config['data_item_template'],\
                    {'slug': data_dict['slug'], 'type': data_dict['type'],\
                    'value': data_dict['value']}))

    return renderer.render(adapter_config['body_template'], {'week': week,\
            'facility': facility, 'data_items': data_items,\
            'report_date': datetime.datetime.now().isoformat()})

def _build_uri(adapter_config):
    uri = uritemplate.expand(URI_TEMPLATE, adapter_config)
    return uri

def _build_dhis_auth_token(adapter_config):
    return base64.b64encode("%s:%s" % (adapter_config['user'], adapter_config['pass']))

def dhis_xml(params, adapter_config):
    """
    curl -H "Content-Type: application/json" -d '{"url": "http://localhost:8080/", "adapter_config": "dhis_config", "adapter": "dhis_xml", "result_callback_url": "http://localhost:8080/callback/", "params": {"week": "42", "data": [{"type": "wat", "slug": "foo", "value": "8"}], "facility": "foo"}, "countdown": "7"}' http://localhost:8088/queue
    """
    if adapter_config is not None:
        if adapter_config.upper() in globals():
            dconfig = globals().get(adapter_config.upper())
    else:
        raise dispatcher.TaskFailure('No adapter configuration named: %s' % adapter_config)
    data = json.loads(params)
    xml_payload_str = _build_dhis_xml_payload(dconfig, data.get('week'), data.get('facility'), data.get('data'))
    uri = _build_uri(dconfig)
    auth_token = _build_dhis_auth_token(dconfig)
    headers = {
        "Content-type": "application/xml",
        "Authorization": "Basic %s" % (auth_token)
    }
    return uri, headers, xml_payload_str

def foo_json(params, adapter_config):
    """
    curl -H "Content-Type: application/json" -d '{"url": "http://localhost:8080/", "adapter_config": "foo_config", "adapter": "foo_json", "result_callback_url": "http://localhost:8080/callback/", "params": {"week": "42", "data": [{"type": "wat", "slug": "foo", "value": "8"}], "facility": "foo"}, "countdown": "7"}' http://localhost:8088/queue
    """
    if adapter_config is not None:
        if adapter_config.upper() in globals():
            fconfig = globals().get(adapter_config.upper())
    else:
        raise dispatcher.TaskFailure('No adapter configuration named: %s' % adapter_config)
    uri = _build_uri(fconfig)
    data = json.loads(params)
    json_payload_obj = _build_foo_json_payload(fconfig, data.get('week'), data.get('facility'), data.get('data'))
    json_payload_str = json.dumps(json_payload_obj)
    headers = {
        "Content-type": "application/json",
    }
    return uri, headers, json_payload_str
