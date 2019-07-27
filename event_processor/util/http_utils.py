import requests
import json
from requests.adapters import HTTPAdapter

class HttpUtils:

    @staticmethod
    def get_session(default_headers=None, convert_snake_case=True):
        session = requests.Session()

        if default_headers is not None:
            session.headers.update(default_headers)

        adapter = RequestAdapter(convert_snake_case)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        return session

class RequestAdapter(HTTPAdapter):
    def __init__(self, convert_snake_case):
        self.convert_snake_case = convert_snake_case
        super(RequestAdapter, self).__init__()

    def send(self, request, *args, **kwargs):
        if request.body is not None and self.convert_snake_case:
            body = json.loads(request.body)
            request.prepare_body(None, None, self.obj_keys_to_camel_case(body))
        return super(RequestAdapter, self).send(request, *args, **kwargs)

    def obj_keys_to_camel_case(self, snake_obj):
        if isinstance(snake_obj, list):
            return [self.obj_keys_to_camel_case(val) for val in snake_obj]
        if isinstance(snake_obj, dict):
            return {self.to_camel_case(key): self.obj_keys_to_camel_case(value) for key, value in snake_obj.items()}
        return snake_obj

    def to_camel_case(self, snake_str):
        first, *rest = snake_str.split('_')
        return first + ''.join(word.capitalize() for word in rest)
        