import logging

from django.core.paginator import Paginator
from django.db import transaction

from signin.utils.exception import UserNotFoundException, BadRequestException
from .models import Users, UsersProfile, UsersFavoriteSearch
from .utils.encrypt import hash_string
from .utils.exception import DatabaseErrorException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@transaction.atomic
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    name = request.data.get('name')
    email = request.data.get('email')
    line_user_id = request.data.get('line_user_id')
    role = 'undefined'
    try:
        existing_user = Users.objects.filter(username=username)
        existing_email = UsersProfile.objects.filter(email=email)
    except Exception as e:
        logger.error(e)
        raise DatabaseErrorException
    if len(existing_user) > 0 or len(existing_email) > 0:
        raise BadRequestException('Username already exists')

    hashed_password, salt = hash_string(password)
    try:
        u = Users(username=username, password=hashed_password, salt=salt, role=role, line_user_id=line_user_id)
        u.save()
        user_profile = UsersProfile(user=u, name=name, email=email)

        user_profile.save()
    except Exception as e:
        print(e)
        raise DatabaseErrorException


def get_user_favorite_search_by_user_id(id):
    users = Users.objects.filter(id=id)
    if len(users) == 0:
        raise UserNotFoundException
    user_favorite_search = UsersFavoriteSearch.objects.filter(user=users[0])
    return user_favorite_search


def create_user_favorite_search(request):
    username = request.username
    price_from = request.data.get('price_from') or 0
    price_to = request.data.get('price_to') or 100000000
    space_from = request.data.get('space_from') or 0
    space_to = request.data.get('space_to') or 999
    room_from = request.data.get('room_from') or 0
    room_to = request.data.get('room_to') or 99
    toilet_from = request.data.get('toilet_from') or 0
    toilet_to = request.data.get('toilet_to') or 99
    floor_from = request.data.get('floor_from') or 0
    floor_to = request.data.get('floor_to') or 99
    location = request.data.get('location')

    users = Users.objects.filter(username=username)

    if len(users) == 0:
        raise UserNotFoundException

    try:
        user_favorite_serach = UsersFavoriteSearch(user=users[0], price_from=price_from, price_to=price_to,
                                                   space_from=space_from,
                                                   space_to=space_to, room_from=room_from, room_to=room_to,
                                                   toilet_from=toilet_from, toilet_to=toilet_to
                                                   , floor_from=floor_from, floor_to=floor_to, location=location)
        user_favorite_serach.save()
    except Exception as e:
        print(e)
        raise DatabaseErrorException


def filter_user_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    tier = request.GET.get('tier', 0)
    try:
        users = Users.objects.filter(tier=tier)
        ret = users[page_size * (page - 1):page_size * page]
    except Exception as e:
        print(e)
        raise DatabaseErrorException
    return ret
