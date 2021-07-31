from django.urls import path
from . import views

app_name = 'posteq'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('post_list/', views.PostListView.as_view(), name = 'post_list'),
    path('post_page/', views.PostEqView.as_view(), name = 'post_page'),
    path('skill_query/', views.SkillQuery, name = 'skill_query'),
    path('confirm/', views.PostToEq, name = 'post_to_confirm'),
    path('post_confirm/', views.PostConfirm.as_view(), name = 'post_confirm'),
    path('post_register/', views.PostRegister, name = 'post_register'),
    path('post_complete/', views.PostComplete.as_view(), name = 'post_complete'),
    path('test/<int:pk>/', views.TestView.as_view(), name = 'test'),
    path('<int:pk>/like/', views.like, name = 'like'),
    path('save_eq/', views.SaveEQ, name = 'save_eq'),

    path('post_clip/', views.PostClipView.as_view(), name = 'post_clip'),
    path('clip_to_confirm/', views.ClipToEq, name = 'clip_to_confirm'),
    path('save_to_clip/', views.SaveToClip, name = 'save_to_clip'),
    path('links/', views.LinksView.as_view(), name = 'links'),

    # path('statistics/', views.StatView.as_view(), name = 'statistics'),
    # path('tweetoauth', views.TweetAPI, name = 'oauth'),
    # path('tweet', views.TweetFormView.as_view(), name = 'tweet'),
    # path('tweet_post', views.TweetPost, name = 'tweet_post'),
    # path('tweet_result', views.TweetResultView.as_view(), name = 'tweet_result'),
]
