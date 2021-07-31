import hashlib
from ..models import User

def hash(str):
    return hashlib.sha256(str.encode()).hexdigest()

"""クッキーとユーザーの認証が整合するかチェック"""
def auth_validate(request, UserModel):
    access_token=request.COOKIES['uso']
    if (UserModel.access_token == hash(access_token)):
        res=True
    else:
        res=False
    return res
"""
セッションのIDからUserモデルを抽出
認証のチェックも行う。認証が正しくなければNoneを返す。
"""
def get_user_from_cookie(request):
    loggedin = False
    try:
        id=request.COOKIES['gerogero']
    except KeyError:
        res = None
    else:
        if id != "":
            try:
                res=User.objects.get(id=id)
            except User.DoesNotExist:
                res = None
            else:
                if auth_validate(request, res):
                    loggedin = True
                else:
                    res = None
        else:
            res = None
    return res, loggedin
