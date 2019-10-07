import requests
import json
from requests.adapters import HTTPAdapter

class HttpUtils:

    @staticmethod
    def get_session(default_headers=None, convert_snake_case=True):
        """??? Get the session for the given crawler of the session?"""
        session = requests.Session()

        if default_headers is not None:
            session.headers.update(default_headers)

        adapter = RequestAdapter(convert_snake_case)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        return session

class RequestAdapter(HTTPAdapter):
    """??? Class representing an HTTP adaptder for a crawler"""
    def __init__(self, convert_snake_case):
        self.convert_snake_case = convert_snake_case
        super(RequestAdapter, self).__init__()

    def send(self, request, *args, **kwargs):
        """??? Send an http request with this adapter"""
        if request.body is not None and self.convert_snake_case:
            body = json.loads(request.body)
            request.prepare_body(None, None, self.obj_keys_to_camel_case(body))
        return super(RequestAdapter, self).send(request, *args, **kwargs)

    def obj_keys_to_camel_case(self, snake_obj):
        """Convert all keys inside the given snake to camel case (why?)"""
        if isinstance(snake_obj, list):
            return [self.obj_keys_to_camel_case(val) for val in snake_obj]
        if isinstance(snake_obj, dict):
            return {self.to_camel_case(key): self.obj_keys_to_camel_case(value) for key, value in snake_obj.items()}
        return snake_obj

    def to_camel_case(self, snake_str):
        """Internal utlity function to convert a string into camel case"""
        first, *rest = snake_str.split('_')
        return first + ''.join(word.capitalize() for word in rest)
        