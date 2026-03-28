from django.urls import path, include
from user import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path('users/', include('django.contrib.auth.urls')),
    path('users/sign_up', views.SignUpView.as_view(), name='sign_up'),
]