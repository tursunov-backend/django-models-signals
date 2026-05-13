from django.urls import path

from .views import UsersView, ProfileView


urlpatterns = [
    path('users/', UsersView.as_view(), name='users'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
]