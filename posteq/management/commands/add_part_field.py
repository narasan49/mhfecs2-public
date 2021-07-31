from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from ...models import EqData, JewelData, CuffData, DataOfEq
import numpy as np
# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help regist_modelで表示されるメッセージ
    help = ''

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):

        jewels = JewelData.objects.all()
        for jewel in jewels:
            jewel.data.part = "jewel"
            jewel.data.save()

        cuffs = CuffData.objects.all()
        for cuff in cuffs:
            cuff.data.part = "cuff"
            cuff.data.save()
