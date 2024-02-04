from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('login_page',views.login_page, name="login_page"),
    path('userprofiles/', views.user_profiles, name='user_profiles'),
]
