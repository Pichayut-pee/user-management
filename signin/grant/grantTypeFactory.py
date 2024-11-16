from .grantType import GrantType
from .passwordGrant import PasswordGrant


class GrantTypeFactory:

    @staticmethod
    def getGrantType(grant_type):
        if GrantType(grant_type) is GrantType.PASSWORD:
            return PasswordGrant()
        else:
            return None

