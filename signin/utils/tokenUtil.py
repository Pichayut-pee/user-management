import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os
from signin.utils.exception import AuthenticationException, ServerErrorException
from django_redis import get_redis_connection

load_dotenv()


class TokenUtils:
    def __init__(self):
        load_dotenv()
        self.redis_conn = get_redis_connection("default")

    def generate_oauth_token(self,sub,user_id):
        tz = timezone(timedelta(hours=7))

        access_token = jwt.encode({'iss': "authorization-server",
                                   'user_id': user_id,
                                   'sub': sub,
                                   "aud": "example.com",
                                   "exp": datetime.now(tz=tz) + timedelta(
                                       seconds=int(os.getenv("ACCESS_TOKEN_EXPIRE_SECOND"))),
                                   "iat": datetime.now(tz=tz),
                                   "jit": sub,
                                   "permission": []
                                   }
                                  , os.getenv("TOKEN_SECRET"), algorithm='HS256')

        refresh_token = jwt.encode({'iss': "authorization-server",
                                    'sub': sub,
                                    "aud": "example.com",
                                    "exp": datetime.now(tz=tz) + timedelta(
                                        seconds=int(os.getenv("REFRESH_TOKEN_EXPIRE_SECOND"))),
                                    "iat": datetime.now(tz=tz),
                                    "jit": sub,
                                    "permission": []
                                    }
                                   , os.getenv("TOKEN_SECRET"), algorithm='HS256')

        return access_token, refresh_token

    def decode_token(self, token):
        try:
            claims = jwt.decode(token, os.getenv("TOKEN_SECRET"), algorithms=["HS256"],
                                options={"verify_aud": False, "verify_signature": True}, )
            return claims
        except jwt.exceptions.InvalidTokenError as e:
            raise AuthenticationException('Invalid token')
        except Exception:
            raise ServerErrorException('Unhandled token extraction error')

    def is_valid_token(self, token):
        # extract token
        claims = self.decode_token(token)
        sub = claims['sub']
        user_id = claims['user_id']

        stored_token = self.redis_conn.get(sub + "access_token") or self.redis_conn.get(sub + "refresh_token")
        stored_token = stored_token.decode(encoding="utf-8")
        if stored_token is None or stored_token != token:
            return False

        return True, sub, user_id

    def revoke_token(self, token):
        # extract token
        claims = self.decode_token(token)
        sub = claims['sub']

        self.redis_conn.delete(sub + "access_token")
        self.redis_conn.delete(sub + "refresh_token")
