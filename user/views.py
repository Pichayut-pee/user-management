import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from signin.utils.decorator import client_validate, authentication
from signin.utils.exception import BadRequestException
from user.services import register_user, create_user_favorite_search, \
    get_user_favorite_search_by_user_id, filter_user_list
from django.http import JsonResponse
from django.template import loader
from django.http import HttpResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@api_view(['POST'])
@client_validate
def register(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        email = request.data.get('email')
        line_user_id = request.data.get('line_user_id')
        register_user(username, password, name, email, line_user_id)
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
        favorite_search_id = request.data.get('favorite_id') or -1
        user_id = request.user_id
        price_from = request.data.get('price_from').replace(',', '') or 1
        price_to = request.data.get('price_to').replace(',', '') or 100000000
        space_from = request.data.get('space_from') or -1
        space_to = request.data.get('space_to') or 999
        room_from = request.data.get('room_from') or -1
        room_to = request.data.get('room_to') or 99
        toilet_from = request.data.get('toilet_from') or -1
        toilet_to = request.data.get('toilet_to') or 99
        floor_from = request.data.get('floor_from') or -1
        floor_to = request.data.get('floor_to') or 99
        desc_search = request.data.get('desc_search')
        location = request.data.get('location')
        limit = request.data.get('limit') or 20
        create_user_favorite_search(favorite_search_id
                                    , user_id
                                    , price_from
                                    , price_to
                                    , space_from
                                    , space_to
                                    , room_from
                                    , room_to
                                    , toilet_from
                                    , toilet_to
                                    , floor_from
                                    , floor_to
                                    , desc_search
                                    , location
                                    , limit)
        return Response('Created', status=201)
    except Exception as e:
        logger.error(e)
        return Response('Internal server error', status=500)


@api_view(['GET'])
@client_validate
def get_favorite_search(request):
    user_id = request.GET.get('user_id')
    favorite_search = get_user_favorite_search_by_user_id(user_id)
    if len(favorite_search) == 0:
        return JsonResponse({}, safe=False)
    return JsonResponse([ret.serialize() for ret in favorite_search], safe=False)


@api_view(['GET'])
@client_validate
def get_user_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    tier = request.GET.get('tier', 0)
    rets = filter_user_list(page, page_size, tier)
    return JsonResponse([ret.serialize() for ret in rets], safe=False)


@api_view(['GET'])
@authentication
def user_favorite_search_page(request):
    temp_favorite_search = get_user_favorite_search_by_user_id(request.user_id)
    favorite_search = [ret.serialize() for ret in temp_favorite_search]

    if len(favorite_search) == 0:
        favorite_search = [None, None]
    elif len(favorite_search) == 1:
        favorite_search = [favorite_search[0], None]

    context = {"favorite_search_1": favorite_search[0], "favorite_search_2": favorite_search[1] }
    template = loader.get_template('user_favorite_search_page.html')

    return HttpResponse(template.render(context, request))
