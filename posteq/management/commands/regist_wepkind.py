from django.core.management.base import BaseCommand
from ...models import WepKind
# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help regist_modelで表示されるメッセージ
    help = ''

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        #print(args)
        wep_kinds = ["片手剣", "双剣", "大剣", "太刀", "ハンマー", "狩猟笛",
                     "ランス", "ガンランス", "穿龍棍", "スラッシュアックスF", "マグネットスパイク",
                     "ライトボウガン", "ヘヴィボウガン", "弓",
                     "剣士汎用", "ガンナー汎用"
                    ]
        short_name = ["片手", "双剣", "大剣", "太刀", "槌", "笛",
                     "槍", "銃槍", "棍", "剣斧", "斬槌",
                     "軽銃", "重銃", "弓",
                     "剣汎", "ガ汎"
                    ]

        wpk = WepKind.objects.all()
        registed_name = [wpki.name for wpki in wpk]
        for i in range(len(wep_kinds)):
            if not wep_kinds[i] in registed_name:
                ph = WepKind(name=wep_kinds[i], short_name=short_name[i])
                ph.save()
