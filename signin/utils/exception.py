
class AuthenticationException(Exception):

    def __init__(self, message="Invalid credential"):
        self.message = message
        super().__init__(self.message)
class UserNotFoundException(Exception):

    def __init__(self, message="Invalid credential"):
        self.message = message

class DuplicateUserException(Exception):

    def __init__(self, message="User already exists"):
        self.message = message

class BadRequestException(Exception):

    def __init__(self, message="Invalid request"):
        self.message = message

class ServerErrorException(Exception):

    def __init__(self, message="Something went wrong"):
        self.message = message
        super().__init__(self.message)
