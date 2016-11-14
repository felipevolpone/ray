
try:
    from urllib import parse
except Exception as e:
    import urlparse as parse


def param_at(url, index):
    """
        index starts after the word after api.
        Example: /api/user/123, index 2 returns 123
        Example: /api/user/foo/123, index 1 returns user, index 2 returns foo
    """
    if url and url[0] == '/':
        url = url[1:]

    url = url.replace('api/', '')

    if index > 0:
        index -= 1
    elif index == 0:
        return None

    params = url.split('/')
    if len(params) > index:
        return params[index]

    return None


def get_id(url):
    return param_at(url, 2)


def query_params_to_dict(request):
    params_with_array = parse.parse_qs(request.query_string)
    params = {}
    for key, values in params_with_array.items():
        value = values[0]
        try:
            value = int(values[0])
        except:
            pass
        params[key] = value
    return params


def get_parameters(request):
    if request.method.lower() == 'get' or request.method.lower() == 'delete':
        return request.params

    elif request.method.lower() == 'post' or request.method.lower() == 'put':
        if request.json:
            return request.json
