"""
URL configuration for login project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from signin import views as signin_view
from user import views as user_view

urlpatterns = [

    path('login_page', signin_view.login_page),
    path('login', signin_view.login),
    path('validate_token', signin_view.validate_token),
    path('logout', signin_view.logout),
    path('line/redirect', signin_view.redirect_signup_line),

    path('favorite_search', user_view.create_favorite_search),
    path('register', user_view.register),
    path('user/list', user_view.get_user_list),

]
