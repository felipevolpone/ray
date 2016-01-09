import json

_ENCODE = 'utf-8'


def from_list(models):
    return [model.to_json() for model in models]


def from_json(inst, encoding=_ENCODE):
    return json.dumps(inst, encoding=_ENCODE)


def to_json(text, encoding=_ENCODE, will_decode=True):
    json_dict = json.loads(text, encoding=_ENCODE)
    if will_decode:
        return decode(json_dict)
    return json_dict


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode(_ENCODE)
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = decode(item)
        rv.append(item)
    return rv


def decode(data):
    if isinstance(data, list):
        return _decode_list(data)

    rv = {}
    if not data:
        return rv

    if isinstance(data, unicode):
        return data.encode(_ENCODE)

    if isinstance(data, str) or isinstance(data, int) or isinstance(data, long):
        return data

    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode(_ENCODE)
        if isinstance(value, unicode):
            value = value.encode(_ENCODE)
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = decode(value)
        rv[key] = value
    return rv
