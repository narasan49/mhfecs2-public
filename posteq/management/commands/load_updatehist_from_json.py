from django.core.management.base import BaseCommand
from posteq.models import UpdateHist
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

        hists = data["update_hist"]
        for hist in hists:
            pos_date = datetime.datetime.strptime(hist["date"], '%Y年%m月%d日%H:%M')
            u = UpdateHist(date=pos_date,
                     datver=hist["datver"],
                     errors=hist["errors"],
                     others=hist["others"],
                     )
            u.save()
