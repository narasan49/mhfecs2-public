from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse,HttpResponseRedirect, Http404
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
from requests_oauthlib.oauth1_session import TokenRequestDenied
from django.conf import settings
from user import APIconfig
from posteq.models import EQ, WepKind
from .models import User
# from .functions import auth_validate, get_user_from_session
import json
import random
import numpy as np
from .functions.misc import hash, get_user_from_cookie
from .forms import UserProfile
# Create your views here.
class UserCreate(generic.TemplateView):
    template_name = 'user/create.html'

def TwitterApprove(request):
    """
    アプリの承認
    """
    CK = APIconfig.CONSUMER_KEY
    CS = APIconfig.CONSUMER_SECRET
    twitter = OAuth1Session(CK,client_secret=CS) #認証処理
    request_token_url = "https://api.twitter.com/oauth/request_token"

    if settings.DEBUG:
        oauth_callback = 'http://127.0.0.1:8000/user/signup'
    else:
        oauth_callback = 'https://narasan.coresv.com/user/signup'
    resRequestToken = twitter.fetch_request_token(request_token_url, params={'oauth_callback': oauth_callback})

    authorization_url = 'https://api.twitter.com/oauth/authorize'
    authURL = twitter.authorization_url(authorization_url)
    return HttpResponseRedirect(authURL)

def TwitterSignup(request):
    """
    アプリの承認後、会員登録またはログインする
    """
    CK = APIconfig.CONSUMER_KEY
    CS = APIconfig.CONSUMER_SECRET
    max_age = 30*24*3600

    access_token_url = 'https://api.twitter.com/oauth/access_token'
    twitter = OAuth1Session(CK,client_secret=CS)
    redirect_response = request.get_full_path()
    res = twitter.parse_authorization_response(redirect_response)

    try:
        res_access_token = twitter.fetch_access_token(access_token_url)
    except TokenRequestDenied:
        status_code=401
        status_text="認証に失敗しました。初めからやり直してください。"
    except:
        status_code=999
        status_text="認証に関する予期しないエラーです。管理者に問い合わせてください。"
    else:
        token=hash(res_access_token["oauth_token"])
        token_secret = hash(res_access_token["oauth_token_secret"])
        print(res_access_token["oauth_token"])
        print(token)
        #登録済みかどうか判定
        try:
            user=User.objects.get(access_token=token, access_token_secret=token_secret)
        except User.DoesNotExist:
            #新規登録
            newComer = User(access_token=token, access_token_secret=token_secret)
            newComer.save()
            response = redirect("user:profile")
            #セッションにトークンを保存
            response.set_cookie("gerogero", value=newComer.id, max_age=max_age)
            response.set_cookie("uso", value=res_access_token["oauth_token"], max_age=max_age)
            # response.set_cookie("_mhf2", value=token_secret, max_age=max_age)
            return response
        else:
            response = redirect("user:mypage", user.id)
            #セッションにトークンを保存
            # response.set_cookie("_mhf2", value=token_secret, max_age=max_age)
            response.set_cookie("uso", value=res_access_token["oauth_token"], max_age=max_age)
            response.set_cookie("gerogero", value=user.id, max_age=max_age)
            return response

    return render(request, 'user/errors.html', {'status_text':status_text, 'status_code':status_code})

class Profile(generic.FormView):
    form_class = UserProfile
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user, loggedin = get_user_from_cookie(self.request)
        context["user"] = user
        context["loggedin"] = loggedin
        if not loggedin:
            context["message"]="はじめに会員登録またはログインしてください。"
        return context

    def form_valid(self, form):
        # user, loggedin = get_user_from_cookie(self.request)
        id=self.request.COOKIES['gerogero']
        user = User.objects.get(id=id)
        user.name = self.request.POST["name"]
        user.self_introduce = self.request.POST["self_introduce"]
        if (user.Url != self.request.POST["Url"]):
            user.UrlIfChecked = False
        user.Url = self.request.POST["Url"]
        user.UrlTitle = self.request.POST["UrlTitle"]
        user.UrlDescription = self.request.POST["UrlDescription"]
        user.save()
        response = redirect("user:mypage", id)
        return response

class MyPage(generic.DetailView):
    model = User
    template_name = 'user/mypage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        context["latest"] = self.object.postedeqs.order_by('-pos_date')[0:1]
        if own != None:
            if own.id == 1:
                context["check_user"] = User.objects.filter(UrlIfChecked=False)

        wep_kinds=WepKind.objects.all()
        eq = self.object.postedeqs.all()
        data = []
        for wep in wep_kinds:
            data.append(eq.filter(wep_kind=wep).count())

        context["labels"] = [wep_kind.name for wep_kind in wep_kinds]
        context["labels_short"] = [wep_kind.short_name for wep_kind in wep_kinds]
        context["data"] = data
        return context

class MyPagePostedeqs(generic.DetailView):
    model = User
    template_name = 'user/postedeqs.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context

class MyPageSavedeqs(generic.DetailView):
    model = User
    template_name = 'user/savedeqs.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context

class FollowList(generic.DetailView):
    model = User
    template_name = 'user/followlist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context

class FollowerList(generic.DetailView):
    model = User
    template_name = 'user/followerlist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context

def FollowUser(request, pk):
    UserToFollow=User.objects.get(id=pk) #フォローしたい/解除したいユーザー
    own, loggedin = get_user_from_cookie(request)
    if own != None:
        if UserToFollow in own.follow.all():
            own.follow.remove(UserToFollow)
            response = json.dumps({'text':"フォローする", 'id':pk})
        else:
            own.follow.add(UserToFollow)
            response = json.dumps({'text':"フォロー中", 'id':pk})
    own.save()

    return HttpResponse(response,content_type="text/javascript")

class UserLinks(generic.TemplateView):
    template_name = 'user/user_links.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        users_with_url = User.objects.filter(UrlIfChecked=True)
        indices = [i for i in range(len(users_with_url))]
        selected_indices = random.sample(indices, np.min([10,len(users_with_url)]))
        selected_users = []
        for i in selected_indices:
            selected_users.append(users_with_url[i])
        context["SelectedUsers"] = selected_users
        return context

class Terms(generic.TemplateView):
    template_name = 'user/terms.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context

class Policy(generic.TemplateView):
    template_name = 'user/policy.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context
