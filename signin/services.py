import string

from user.models import Users
from .grant.grantTypeFactory import GrantTypeFactory
from dotenv import load_dotenv
import os
from django_redis import get_redis_connection

from .utils.exception import AuthenticationException, DuplicateUserException
from .utils.tokenUtil import TokenUtils

import requests as api_request
import random

class SigninService:

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redis_conn = get_redis_connection("default")
        self.token_util = TokenUtils()
        self.line_redirect_url = os.getenv("LINE_REDIRECT_URL")
        self.line_client_id = os.getenv("LINE_CLIENT_ID")
        self.line_client_secret = os.getenv("LINE_CLIENT_SECRET")
        self.line_token_url = os.getenv("LINE_TOKEN_REQUEST_URL")
        self.line_profile_url = os.getenv("LINE_PROFILE_REQUEST_URL")

    def login(self, request):
        grant_type = request.data.get('grant_type')

        grant = GrantTypeFactory.getGrantType(grant_type)
        access_token, refresh_token = grant.login(request)

        return access_token, refresh_token

    def logout(self, token):
        self.token_util.revoke_token(token)

    def validate_token(self, token):
        # extract token
        is_token_valid,sub = self.token_util.is_valid_token(token)
        if not is_token_valid:
            raise AuthenticationException('Invalid token')
        return True, sub

    def get_line_userprofile(self, request):
        code = request.GET.get('code')

        # Todo: Implement state validation
        state = request.GET.get('state')

        token_request_body = {"grant_type": "authorization_code"
            , "code": code
            , "client_id": self.line_client_id
            , "client_secret": self.line_client_secret
            , "redirect_uri": self.line_redirect_url
                              }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response_token = api_request.post(self.line_token_url, data=token_request_body, headers=headers)
        line_id_token = response_token.json()['id_token']

        line_profile_request_body = {"id_token": line_id_token
            , "client_id": self.line_client_id}

        response_profile = api_request.post(self.line_profile_url, data=line_profile_request_body, headers=headers)
        profile_claims = response_profile.json()
        line_user_id = profile_claims['sub']

        users = Users.objects.filter(line_user_id=line_user_id)
        if len(users) > 0:
            raise DuplicateUserException('User already exists')

        return profile_claims

    def state_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        random_string = ''.join(random.choice(chars) for _ in range(size))
        self.redis_conn.set(random_string, random_string, '600')
        return random_string

