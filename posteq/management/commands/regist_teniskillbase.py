from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from ...models import TeniSkillBase, AbilityDetail
from posteq.functions.regist_db import (
    get_or_create_teniskilldetail,
    )
# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help regist_modelで表示されるメッセージ
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        #print(args)
        print(options['file'])
        file = options['file'][0]
        tmp = file.split("/")
        if tmp[-1] == "TeniSkillBase.xml":
            model = TeniSkillBase

        """
        <Skill>
          <SkillType TypeName="辿異スキル">
            <SkillTree No="1" ID="0010" Name="スキル枠拡張">
              <Skill Point="7">スキル枠拡張+7</Skill>
              <Skill Point="6">スキル枠拡張+6</Skill>
              <Skill Point="5">スキル枠拡張+5</Skill>
              <Skill Point="4">スキル枠拡張+4</Skill>
              <Skill Point="3">スキル枠拡張+3</Skill>
              <Skill Point="2">スキル枠拡張+2</Skill>
              <Skill Point="1">スキル枠拡張+1</Skill>
            </SkillTree>
            <SkillTree No="2" ID="0020" Name="閃転強化" Target="閃転">
              <Skill Point="2">閃転強化+2</Skill>
              <Skill Point="1">閃転強化+1</Skill>
            </SkillTree>
        """
        tree = ET.parse(file)
        root = tree.getroot()
        data = []
        for EachType in root:
            for d in EachType:
                # print(d.attrib)
                name      = d.attrib["Name"]
                id        = int(d.attrib["No"])
                priority  = int(d.attrib["ID"])
                skill_detail = []
                for skills in d:

                    skill_detail.append({"active_skill":skills.text,
                                         "active_point":int(skills.attrib["Point"]),
                                         })
                each = {"name":name,
                "id":id,
                "priority":priority,
                "active_skills":skill_detail,
                }
                data.append(each)
        for eq_data in data:
            """既存かどうかチェック"""
            sb = TeniSkillBase.objects.filter(name=eq_data["name"])
            print(eq_data["name"])
            if sb.exists():
                is_already = True
                """doeに変更があるなら反映させる"""
                sb = sb[0]
                if sb.id != eq_data["id"]:
                    print("ID of "+eq_data["name"]+" has changed!!!")
                    exit()
                sb.priority = eq_data["priority"]
                sb.save()
            else:
                """存在しない"""
                is_already = False

            if not is_already:
                """新規"""
                sb = TeniSkillBase(name=eq_data["name"], priority=eq_data["priority"], id=eq_data["id"])
                sb.save()
                #active_skills
                for ac in eq_data["active_skills"]:
                    skill=ac["active_skill"]
                    point=ac["active_point"]
                    skill_detail = get_or_create_teniskilldetail(skill, point)
                    skill_detail.save()
                    sb.active_abilities.add(skill_detail)

                sb.save()
            else:
                """変更があるかどうか確認"""
                sb = TeniSkillBase.objects.get(name=eq_data["name"])
                active_skills = sb.active_abilities.all().values("active_skill","active_point")
                if active_skills:
                    for ac in eq_data["active_skills"]:
                        skill=ac["active_skill"]
                        point=ac["active_point"]
                        is_changed=True
                        for each in active_skills:
                            if (each["active_skill"]==skill) and (each["active_point"]==point):
                                is_changed=False
                        if is_changed:
                            skill_detail = get_or_create_teniskilldetail(skill, point)
                            skill_detail.save()
                            sb.active_abilities.remove(sb.active_abilities.filter(active_skill=skill)[0])
                            sb.active_abilities.add(skill_detail)
                sb.save()
