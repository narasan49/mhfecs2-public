from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login_create/', views.UserCreate.as_view(), name = 'login_create'),
    path('oauth/', views.TwitterApprove, name = 'oauth'),
    path('signup/', views.TwitterSignup, name = 'signup'),
    path('profile/', views.Profile.as_view(), name = 'profile'),

    path('mypage/<int:pk>/', views.MyPage.as_view(), name = 'mypage'),
    path('mypage/<int:pk>/postedeqs/', views.MyPagePostedeqs.as_view(), name = 'postedeqs'),
    path('mypage/<int:pk>/savedeqs/', views.MyPageSavedeqs.as_view(), name = 'savedeqs'),
    path('mypage/<int:pk>/followerlist/', views.FollowerList.as_view(), name = 'followerlist'),
    path('mypage/<int:pk>/followlist/', views.FollowList.as_view(), name = 'followlist'),

    path('followuser/<int:pk>/', views.FollowUser, name = 'followuser'),
    path('terms/', views.Terms.as_view(), name = 'terms'),
    path('policy/', views.Policy.as_view(), name = 'policy'),
    path('user_links/', views.UserLinks.as_view(), name = 'user_links'),

    # path('errors/', views.ErrorPage.as_view(), name = 'errors'),
]
