DHIS = {\
        "protocol" : 'http',
        "domain" : ['localhost'],
        "port" : ":8080",
        "path" : ['dhis','api'],
        "user": 'sekiskylink',
        "pass": '123Congse',
        "body_template" : """
        <?xml version='1.0' encoding='UTF-8'?>
        <dataValueSet completeDate="{{ report_date }}" xmlns="http://dhis2.org/schema/dxf/2.0" period="{{ week }}" orgUnit="{{ facility }}">
          {{ data_items }}
         </dataValueSet>
        """,
        "body_reconcile_tokens": ['facility'],
        "data_item_template": """<dataValue dataElement="{{ slug }}" categoryOptionCombo="{{ type }}" value="{{ value }}"/>""",
        "data_item_reconcile_tokens": ['slug', 'type'],
        "datetime_format": "%F",
        "template_type": "xml"
        }

MY_DHIS = {\
        "protocol" : 'http',
        "domain" : ['localhost'],
        "port" : ":8080",
        "path" : ['dhis','api'],
        "user": 'sekiskylink',
        "pass": '123Congse',
        "body_template" : """
        <?xml version='1.0' encoding='UTF-8'?>
        <dataValueSet completeDate="{{ report_date }}" xmlns="http://dhis2.org/schema/dxf/2.0" period="{{ week }}" orgUnit="{{ facility }}">
          {{ data_items }}
         </dataValueSet>
        """,
        "body_reconcile_tokens": ['facility'],
        "data_item_template": """<dataValue dataElement="{{ slug }}" categoryOptionCombo="{{ type }}" value="{{ value }}"/>""",
        "data_item_reconcile_tokens": ['slug', 'type'],
        "datetime_format": "%F",
        "template_type": "xml"
        }

FOO = {\
        "protocol" : 'http',
        "domain" : ['localhost'],
        "port" : ":8080",
        "path" : ['foo','api'],
        "query" : {'foo': 'bar'},
        "body_template" : """{"week": "{{ week }}", "report_date": "{{ report_date }}", "facility": "{{ facility }}", "data": [{{ data_items }}]}""",
        "data_item_template" : """{"slug": "{{ slug }}", "type": "{{ type }}", "value": "{{ value }}"},""",
        "datetime_format": "%Y-%m-%dT%H:%M:%S.%f",
        "template_type": "json"
        }

URI_TEMPLATE = "{protocol}://{domain*}{+port}{/path*}/{?query*}"

