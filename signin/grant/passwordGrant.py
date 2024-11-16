from user.models import Users
from .grantTokenService import GrantTypeService

from ..utils.encrypt import check_hash
from ..utils.exception import AuthenticationException, ServerErrorException
from django_redis import get_redis_connection
from dotenv import load_dotenv
import os

from ..utils.tokenUtil import TokenUtils


class PasswordGrant(GrantTypeService):

    def __init__(self):
        self.redis_conn = get_redis_connection("default")
        load_dotenv()
        self.access_token_expire = os.getenv('ACCESS_TOKEN_EXPIRE_SECOND')
        self.refresh_token_expire = os.getenv('REFRESH_TOKEN_EXPIRE_SECOND')
        self.token_util = TokenUtils()

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        users = Users.objects.filter(username=username)
        if users is None or len(users) == 0:
            raise AuthenticationException('Invalid username or password')

        hashed_password = users[0].password

        # checking password
        if check_hash(password, hashed_password) is False:
            raise AuthenticationException('Invalid username or password')
        access_token, refresh_token = self.token_util.generate_oauth_token(users[0].username)

        # Store token in redis
        try:

            self.redis_conn.set(username + "access_token", access_token, self.access_token_expire)
            self.redis_conn.set(username + "refresh_token", refresh_token, self.refresh_token_expire)

        except Exception as e:
            print(f"Error occured while inserting the data : {e}")
            raise ServerErrorException("Error connecting to database")

        return access_token, refresh_token
