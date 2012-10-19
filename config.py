DHIS_CONFIG = {\
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
        "data_item_template": """
          <dataValue dataElement="{{ slug }}" categoryOptionCombo="{{ type }}" value="{{ value }}"/>
        """}

FOO_CONFIG = {\
        "protocol" : 'http',
        "domain" : ['localhost'],
        "port" : ":8080",
        "path" : ['foo','api'],
        "query" : {'foo': 'bar'},
        "body_template" : """
            {"week": {{ week }}, "report_date": {{ report_date }}, "facility": {{ facility }}, "data": {{ data_items }}}
        """,
        "data_item_template" : """
            {'slug': '{{ slug }}', 'type': '{{ type }}', 'value': '{{ value }}'}
        """
        }

URI_TEMPLATE = "{protocol}://{domain*}{+port}{/path*}/{?query*}"

