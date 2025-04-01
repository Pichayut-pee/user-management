import logging

from django.core.paginator import Paginator
from django.db import transaction
from django_redis import get_redis_connection

from signin.utils.exception import UserNotFoundException, BadRequestException
from .models import Users, UsersProfile, UsersFavoriteSearch
from .utils.encrypt import hash_string
from .utils.exception import DatabaseErrorException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
redis_conn = get_redis_connection("default")

@transaction.atomic
def register_user(username, password, name, email, line_user_id):

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
    user_favorite_search = UsersFavoriteSearch.objects.filter(user=users[0]).order_by('id')
    return user_favorite_search


def create_user_favorite_search(favorite_search_id
                                , user_id
                                , price_from
                                , price_to
                                , space_from
                                , space_to
                                , room_from
                                , room_to
                                ,toilet_from
                                , toilet_to
                                , floor_from
                                , floor_to
                                , desc_search
                                , location
                                , limit):

    if location is None:
        raise BadRequestException('Location is required')

    users = Users.objects.filter(id=user_id)

    if len(users) == 0:
        raise UserNotFoundException

    # if users[0].tier == 0:
    #     raise BadRequestException('You need to upgrade to premium to use this')
    # if exist update
    try:
        user_favorite_search = UsersFavoriteSearch.objects.filter(user=users[0], id=favorite_search_id)
        if len(user_favorite_search) > 0:
            user_favorite_search[0].price_search_from = price_from
            user_favorite_search[0].price_search_to = price_to
            user_favorite_search[0].space_search_from = space_from
            user_favorite_search[0].space_search_to = space_to
            user_favorite_search[0].room_search_from = room_from
            user_favorite_search[0].room_search_to = room_to
            user_favorite_search[0].toilet_search_from = toilet_from
            user_favorite_search[0].toilet_search_to = toilet_to
            user_favorite_search[0].floor_search_from = floor_from
            user_favorite_search[0].floor_search_to = floor_to
            user_favorite_search[0].location_search = location
            user_favorite_search[0].desc_search = desc_search
            user_favorite_search[0].limit = limit
            user_favorite_search[0].save()

            # clear redis by user id
            redis_conn.delete(str(user_id)+'_'+str(favorite_search_id))

            return
    except Exception as e:
        logger.error(e)
        raise DatabaseErrorException
    # if not exist save
    try:
        user_favorite_search = UsersFavoriteSearch(user=users[0], price_search_from=price_from,
                                                   price_search_to=price_to,
                                                   space_search_from=space_from,
                                                   space_search_to=space_to, room_search_from=room_from,
                                                   room_search_to=room_to,
                                                   toilet_search_from=toilet_from, toilet_search_to=toilet_to
                                                   , floor_search_from=floor_from, floor_search_to=floor_to,
                                                   location_search=location
                                                   , desc_search=desc_search, limit=limit
                                                   )
        user_favorite_search.save()
    except Exception as e:
        logger.error(e)
        raise DatabaseErrorException


def filter_user_list(page, page_size, tier):

    try:
        users = Users.objects.filter(tier=tier)
        ret = users[page_size * (page - 1):page_size * page]
    except Exception as e:
        logger.error(e)
        raise DatabaseErrorException
    return ret
