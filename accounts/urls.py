from django.urls import path, include
from .views import *

urlpatterns = [
    path('home/', home, name="home"),
    path('logout/', logout_user, name="logout"),
    path('login/', login_user, name="login"),
    path('account/', account_user, name="account"),
    path('register/', registration_user, name="register"),
    path('must_authenticate/', must_authenticate_user, name="must_authenticate"),

]
