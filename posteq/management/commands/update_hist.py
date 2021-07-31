from django.core.management.base import BaseCommand
from ...models import UpdateHist
from django.utils import timezone

# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help regist_modelで表示されるメッセージ
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('datver', nargs='?')
        parser.add_argument('file', nargs='?')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):

        file = options["file"]
        if file != None:
            with open(file) as f:
                txt = f.read()
        else:
            txt = ""
        latest = UpdateHist.objects.order_by('-date')

        datver = options["datver"]
        if options["datver"] != None:
            if len(latest) > 0:
                if not latest[0].datver != datver:
                    datver = ""
            else:
                tmp = options["datver"].split("/")
                datver = tmp[-2]
        else:
            datver = ""

        if (len(datver) != 0) or (len(txt) != 0):
            uhist=UpdateHist(datver=datver, date=timezone.now(), others=txt)
            uhist.save()
