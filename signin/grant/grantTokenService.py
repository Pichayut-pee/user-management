from abc import abstractmethod


class GrantTypeService:

    @abstractmethod
    def generateToken(self, request):
        pass
