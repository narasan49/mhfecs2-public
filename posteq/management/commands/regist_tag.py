from django.core.management.base import BaseCommand
from ...models import TagBase
# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help regist_modelで表示されるメッセージ
    help = ''

    # def add_arguments(self, parser):
    #     parser.add_argument('file', nargs='+')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        #print(args)
        tag_names = ["対辿異種", "大討伐", "狩煉道", "狩衛戦", "高難易度用",
                     "不退", "非不退", "秘伝", "非秘伝",
                     "汎用装備", "剛閃9",
                     "採集", "無課金", "初心者向け", "ネタ装備", "見た目重視",
                    ]
        registed_tags=TagBase.objects.all()
        registed_name = [tag.name for tag in registed_tags]
        for tag in tag_names:
            if not tag in registed_name:
                ph = TagBase(name=tag)
                ph.save()
