from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from posteq.models import EQ, WepKind, WepData, EqData, JewelData, CuffData
from posteq.functions.skill import CreateEQ, DeriveEquipData
from posteq.functions.ListMan import EqDict2SkillList, JewelDict2SkillList
from user.models import User
from user.functions.misc import hash
import json
import datetime
import numpy as np
# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help regist_modelで表示されるメッセージ
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        file = options['file'][0]
        with open(file, 'r') as f:
            data = json.load(f) #JSON形式で読み込む

        eqs = data["eqs"]
        users = data["users"]
        User.objects.all().delete()
        EQ.objects.all().delete()
        for user in users:
            if not user["name"]:
                username = ""
            else:
                username = user["name"]

            if not user["self_introduce"]:
                self_introduce = ""
            else:
                self_introduce = user["self_introduce"]
            u = User(id=user["id"],
                     name=username,
                     self_introduce=self_introduce,
                     access_token=user["access_token"],
                     access_token_secret=user["access_token_secret"],
                     Url=user["Url"],
                     UrlTitle=user["UrlTitle"],
                     UrlDescription=user["UrlDescription"],
                     UrlIfChecked=user["UrlIfChecked"],
                     UrlAlertForAdmin=user["UrlAlertForAdmin"],
                     )
            u.save()
        """フォロー"""
        for user in users:
            u = User.objects.get(id=user["id"])
            follow_users = user["follow_users"]
            for follow_user_id in follow_users:
                follow_user = User.objects.get(id=follow_user_id)
                u.follow.add(follow_user)
            u.save()

        for eq in eqs:
            if eq["posted_user_id"]:
                own = User.objects.get(id=eq["posted_user_id"])
            else:
                own = None
            pos_date = datetime.datetime.strptime(eq["pos_date"], '%Y年%m月%d日%H:%M')
            wep_kind=WepKind.objects.get(name=eq["wep_kind"])
            wep_dict = {"wep": eq["wep_name"]}
            eq_dict = {"head":eq["head_name"],
                       "body":eq["body_name"],
                       "arm":eq["arm_name"],
                       "wst":eq["wst_name"],
                       "leg":eq["leg_name"],
                       }
            jewel_dict=eq["jewels"]
            cuff_dict=eq["cuffs"]

            wep, stat, mssg = EqDict2SkillList(wep_dict, WepData)
            eqs, stat, mssg = EqDict2SkillList(eq_dict, EqData)
            jewels, stat, mssg = JewelDict2SkillList(jewel_dict, JewelData)
            cuffs, stat, mssg = JewelDict2SkillList(cuff_dict, CuffData)
            eqdata = DeriveEquipData(wep, eqs, jewels, cuffs)
            eqdata["wep"] = wep
            eqdata["eqs"] = eqs
            eqdata["jewel_dict"] = jewel_dict
            eqdata["cuff_dict"]  = cuff_dict
            eqdata["comment"]=eq["comment"]
            eqdata["tags"]=eq["tags"]
            eqdata["name"]=eq["name"]
            eqdata["wep_kind"]=wep_kind
            PostedEQ = CreateEQ(eqdata, own, pos_date=pos_date)

            saved_users = eq["saved_user_ids"]
            for saved_user in saved_users:
                suser = User.objects.get(id=saved_user)
                PostedEQ.saved_user.add(suser)
            PostedEQ.good=eq["good"]
            PostedEQ.save()
