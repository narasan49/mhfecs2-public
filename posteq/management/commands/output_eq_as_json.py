from django.core.management.base import BaseCommand
from posteq.models import EQ, UpdateHist
from user.models import User
import json
# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help regist_modelで表示されるメッセージ
    help = ''

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        postedeq_all = EQ.objects.all()
        registed_users = User.objects.all()
        updatehist_all = UpdateHist.objects.all()
        print(postedeq_all)
        print(registed_users)
        eqs = []
        for postedeq in postedeq_all:
            if postedeq.posted_user:
                posted_user = postedeq.posted_user.id
            else:
                posted_user = 0
            saved_users = list(postedeq.saved_user.values_list("id", flat=True))

            jewel_dict = {}
            for jewel in postedeq.jewel_data.all():
                try:
                    jewel_name = jewel.jewel_data.data.name
                except AttributeError:
                    jewel_name = "【空き】"
                if jewel_name:
                    jewel_dict[jewel_name] = jewel.num

            cuff_dict = {}
            for cuff in postedeq.cuff_data.all():
                cuff_name = cuff.cuff_data.data.name
                if cuff_name:
                    cuff_dict[cuff_name] = 1

            tag_list = list(postedeq.tags.values_list("name", flat=True))
            eq = {"name":postedeq.posted_user_name,
                  "id":postedeq.id,
                  "posted_user_id": posted_user,
                  "saved_user_ids": saved_users,
                  "wep_name":postedeq.wep_data.data.name,
                  "head_name":postedeq.head_data.data.name,
                  "body_name":postedeq.body_data.data.name,
                  "arm_name":postedeq.arm_data.data.name,
                  "wst_name":postedeq.wst_data.data.name,
                  "leg_name":postedeq.leg_data.data.name,
                  "jewels":jewel_dict,
                  "cuffs":cuff_dict,
                  "tags":tag_list,
                  "comment":postedeq.comment,
                  "good":postedeq.good,
                  "wep_kind":postedeq.wep_kind.name,
                  "pos_date":postedeq.pos_date.strftime('%Y年%m月%d日%H:%M'),
                  }
            eqs.append(eq)
            # print(eq)
            # exit()
        users = []
        for registed_user in registed_users:
            follow_users = list(registed_user.follow.values_list("id", flat=True))
            user = {"name":registed_user.name,
                    "id":registed_user.id,
                    "self_introduce":registed_user.self_introduce,
                    "access_token":registed_user.access_token,
                    "access_token_secret":registed_user.access_token_secret,
                    "follow_users":follow_users,
                    "Url":registed_user.Url,
                    "UrlTitle":registed_user.UrlTitle,
                    "UrlDescription":registed_user.UrlDescription,
                    "UrlIfChecked":registed_user.UrlIfChecked,
                    "UrlAlertForAdmin":registed_user.UrlAlertForAdmin,
                    }
            users.append(user)
            # print(user)
            # exit()
        hists = []
        for updatehist in updatehist_all:
            hist = {"date":updatehist.date.strftime('%Y年%m月%d日%H:%M'),
                    "datver":updatehist.datver,
                    "errors":updatehist.errors,
                    "others":updatehist.others,
                    }
            hists.append(hist)
        res = {"eqs":eqs, "users":users, "update_hist":hists}
        with open('site_data.json','w') as f:
            json.dump(res,f,indent=4, ensure_ascii=False)
