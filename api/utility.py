import requests


def _make_request(request_method, **kwargs):
    if request_method == 'get':
        response = requests.get(**kwargs)

    elif request_method == 'post':
        response = requests.post(**kwargs)

    else:
        raise ValueError(f'Request method "{request_method}" is not supported')

    if response.status_code not in [200, 201, 202]:
        msg = f'Request failed with status code {response.status_code} and message {response.content}'
        raise ConnectionError(msg)

    else:
        return response
