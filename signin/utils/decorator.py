import os
from functools import wraps

from django.http import HttpResponse
from dotenv import load_dotenv

from signin.utils.tokenUtil import TokenUtils

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def authentication(view_function):
    @wraps(view_function)
    def wrap(request, *args, **kwargs):
        token = request.headers.get('Authorization') or request.GET.get('access_token')
        if token is None:
            return HttpResponse('Unauthorized', status=401)
        access_token = token.replace("Bearer ", "")

        try:
            token_util = TokenUtils()
            _,sub = token_util.is_valid_token(access_token)
            request.username = sub
        except Exception as e:
            print('Error:', e)
            return HttpResponse('Internal server error', 500)
        return view_function(request, *args, **kwargs)

    return wrap

def client_validate(view_function):
    @wraps(view_function)
    def wrap(request, *args, **kwargs):
        request_client_id = request.headers.get('ClientId')
        request_client_secret = request.headers.get('ClientSecret')

        if client_id is None or client_secret is None or request_client_id != client_id or request_client_secret != client_secret:
            return HttpResponse('Unauthorized', status=401)
        return view_function(request, *args, **kwargs)

    return wrap