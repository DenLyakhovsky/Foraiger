from django.urls import path
from app.views import Home, AboutSite, UserProfileView, UserUpdateView, EmailChangeView, EmailVerificationView, \
    register, user_login, user_logout, CreateUserAPIView, UpdateUserView, UserViewSet, DetailViewUserAPI

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about', AboutSite.as_view(), name='about'),

    path('profile', UserProfileView.as_view(), name='profile'),

    path('update-user/<int:pk>', UserUpdateView.as_view(), name='update'),
    path('change_email/', EmailChangeView.as_view(), name='change_email'),
    path('verification/', EmailVerificationView.as_view(), name='verification'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('api/create/', CreateUserAPIView.as_view()),
    path('api/read/', UserViewSet.as_view({'get': 'list'})),
    path('api/update/<int:pk>', UpdateUserView.as_view()),
    path('api/detail/<int:pk>', DetailViewUserAPI.as_view()),
]
