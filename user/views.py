import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from signin.utils.decorator import client_validate, authentication
from signin.utils.exception import BadRequestException
from user.services import register_user, create_user_favorite_search, \
    get_user_favorite_search_by_user_id, filter_user_list
from django.http import JsonResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@api_view(['POST'])
@client_validate
def register(request):
    try:
        register_user(request)
        return Response('Created', status=201)
    except BadRequestException as e:
        return Response(str(e), status=400)
    except Exception as e:
        logger.error(e)
        return Response('Internal server error', status=500)


@api_view(['POST'])
@authentication
def create_favorite_search(request):
    try:
        create_user_favorite_search(request)
        return Response('Created', status=201)
    except Exception as e:
        logger.error(e)
        return Response('Internal server error', status=500)


@api_view(['GET'])
@client_validate
def get_favorite_search(request):
    user_id = request.GET.get('user_id')
    favorite_search = get_user_favorite_search_by_user_id(user_id)
    if len(favorite_search) ==0 :
        return JsonResponse({}, safe=False)
    return JsonResponse([ret.serialize() for ret in favorite_search], safe=False)



@api_view(['GET'])
@client_validate
def get_user_list(request):
    rets = filter_user_list(request)
    return JsonResponse([ret.serialize() for ret in rets], safe=False)
