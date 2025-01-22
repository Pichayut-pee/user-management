from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.template import loader
from .services import SigninService
from django.http import HttpResponse
import os
from dotenv import load_dotenv

from .utils.decorator import client_validate
from .utils.exception import AuthenticationException, DuplicateUserException

load_dotenv()


@api_view(['GET'])
def validate_token(request):
    token = request.GET.get('access_token') or request.GET.get('refresh_token')
    if token is None:
        return HttpResponse('Unauthorized', status=401)
    signin_service = SigninService()
    try:
        _,sub = signin_service.validate_token(token)
        return Response(sub)
    except AuthenticationException as e:
        return HttpResponse('Unauthorized', status=401)
    except Exception as e:
        return HttpResponse(e, status=500)


@api_view(['GET'])
def login_page(request):
    line_signup_url = os.getenv("LINE_SIGNUP_URL")
    line_client_id = os.getenv("LINE_CLIENT_ID")
    line_redirect_url = os.getenv("LINE_REDIRECT_URL")
    signin_service = SigninService()
    state = signin_service.state_generator()
    line_signup_url = line_signup_url.format(client_id=line_client_id, redirect_url=line_redirect_url, state=state)
    context = {"client_id": os.getenv("CLIENT_ID"),
               "client_secret": os.getenv("CLIENT_SECRET"),
               "line_signup_url": line_signup_url,
               }
    template = loader.get_template('login_page.html')
    return HttpResponse(template.render(context, request))


@api_view(['POST'])
@client_validate
def login(request):
    try:
        signin_service = SigninService()
        access_token, refresh_token = signin_service.login(request)
        redirect_url = os.getenv("LOGIN_SUCCESS_REDIRECT_URL")
        return JsonResponse(
            {"access_token": access_token, "refresh_token": refresh_token, "redirect_url": redirect_url})
    except AuthenticationException:
        return HttpResponse('Unauthorized', status=401)
    except Exception:
        return HttpResponse('Internal server error', status=500)


@client_validate
def logout(request):
    try:
        token = request.GET.get('access_token')
        signin_service = SigninService()
        signin_service.logout(token)
        redirect_url = os.getenv("CONDO_LOGOUT_REDIRECT_URL")
        return JsonResponse({"redirect_url": redirect_url})
    except AuthenticationException:
        return HttpResponse('Unauthorized', status=401)
    except Exception:
        return HttpResponse('Internal server error', status=500)


def redirect_signup_line(request):
    try:
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        signin_service = SigninService()
        profile_claims = signin_service.get_line_userprofile(request)
        template = loader.get_template('user_register_page.html')
        context = {
            "line_user_id": profile_claims['sub'],
            "client_id": client_id,
            "client_secret": client_secret
        }
    except DuplicateUserException as e:
        template = loader.get_template('login_page.html')
        context = {
            "error_message": e.message
        }
    return HttpResponse(template.render(context, request))
def redirect_signup_line(request):
    try:
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        signin_service = SigninService()
        profile_claims = signin_service.get_line_userprofile(request)
        template = loader.get_template('user_register_page.html')
        context = {
            "line_user_id": profile_claims['sub'],
            "client_id": client_id,
            "client_secret": client_secret
        }
    except DuplicateUserException as e:
        template = loader.get_template('login_page.html')
        context = {
            "error_message": e.message
        }
    return HttpResponse(template.render(context, request))