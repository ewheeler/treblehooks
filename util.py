JSON_CONTENT_TYPES = ['application/json', 'application/json; charset=utf-8', 'application/x-javascript', 'text/javascript', 'text/x-javascript', 'text/x-json']

def walks_like_json(raw_content_type):
    if ';' in raw_content_type:
        content_type = raw_content_type.split(';')[0]
    else:
        content_type = raw_content_type
    if content_type in JSON_CONTENT_TYPES:
        return True
    if 'json' in content_type:
        return True
    if 'javascript' in content_type:
        return True
    if 'ecma' in content_type:
        return True
    return False

FORM_CONTENT_TYPES = ['application/x-www-form-urlencoded', 'application/x-www-form-urlencoded; charset=utf-8']

def talks_like_form(raw_content_type):
    return raw_content_type in FORM_CONTENT_TYPES
