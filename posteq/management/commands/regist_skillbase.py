from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from ...models import SkillBase, SkillDetail
from ...functions.regist_db import (
    get_or_create_skilldetail,
    dict_registed_data,
    dict_input_data,
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
        if tmp[-1] == "SkillBase.xml":
            model = SkillBase

        """
        <Skill>
          <SkillType TypeName="">
            <Data No="206" ID="0140" Name="不退">
              <Option Name="不退ノ構" Point="10">
                <ContainedSkills> (あれば)
                  <Skill Name="火事場力+2" />
                  <Skill Name="斬れ味レベル+1" />
                </ContainedSkills>
                <DeactivateSkills> (あれば)
                  <Skill Name="剛撃+4" />
                  ...
                  <Skill Name="ブチギレ" />
                </DeactivateSkills>
              </Option>
            </Data>

        """
        tree = ET.parse(file)
        root = tree.getroot()
        data = []
        for EachType in root:
            type=EachType.attrib["TypeName"]
            for d in EachType:
                #<Data No="206" ID="0140" Name="不退">
                name      = d.attrib["Name"]
                id        = int(d.attrib["No"])
                priority  = int(d.attrib["ID"])
                try:
                    skillrank = int(d.attrib["SkillRank"])
                except KeyError:
                    skillrank = 0
                skill_detail = []
                for skills in d:
                    contain_skill = []
                    deactive_skill = []
                    ind = 0 #要素番号
                    if ind < len(skills):
                        if skills[0].tag == "ContainedSkills":
                            ind += 1
                            for contain in skills[0]:
                                contain_skill.append(contain.attrib["Name"])
                        if ind < len(skills):
                            if skills[ind].tag == "DeactivateSkills":
                                for deact in skills[ind]:
                                    deactive_skill.append(deact.attrib["Name"])

                    skill_detail.append({"active_skill":skills.attrib["Name"],
                                         "active_point":int(skills.attrib["Point"]),
                                         "deactive":deactive_skill,
                                         "contain":contain_skill,
                                         })
                each = {"name":name,
                "id":id,
                "type":type,
                "priority":priority,
                "skillrank":skillrank,
                "active_skills":skill_detail,
                }
                data.append(each)

        basic_data_keys = ["name", "id", "type", "priority", "skillrank"]
        for sb_data in data:
            """既存かどうかチェック"""
            try:
                sb = SkillBase.objects.get(name=sb_data["name"])
            except SkillBase.DoesNotExist:
                """存在しない。新規作成"""
                print(sb_data["name"], "新規")
                sb = SkillBase()
                for key in basic_data_keys:
                    setattr(sb, key, sb_data[key])
                sb.save()
                #active_skills
                for ac in sb_data["active_skills"]:
                    skill=ac["active_skill"]
                    point=ac["active_point"]
                    skill_detail = get_or_create_skilldetail(skill, point)
                    skill_detail.save()
                    sb.active_skills.add(skill_detail)
                sb.save()
            else:
                """存在している。変更がある場合は更新"""
                if_changed=False
                """基本情報の変更確認"""
                input_basic_data_values = [sb_data[key] for key in basic_data_keys]
                input_basic_data_dict = dict(zip(basic_data_keys, input_basic_data_values))
                registed_basic_data_values = [getattr(sb, key) for key in basic_data_keys]
                registed_basic_data_dict = dict(zip(basic_data_keys, registed_basic_data_values))
                if not registed_basic_data_dict==input_basic_data_dict:
                    """基本情報に変更有"""
                    if_changed=True
                    if registed_basic_data_dict["id"] != input_basic_data_dict["id"]:
                        print("ID of "+eq_data["name"]+" has changed!!!")
                        exit()
                    for key in basic_data_keys:
                        setattr(sb, key, input_basic_data_dict[key])

                """スキルの変更確認。contain, deactiveの確認は後回し"""
                registed_skill = dict_registed_data(sb, "active_skills", "active_skill", "active_point")
                input_skill = dict_input_data(sb_data, "active_skills", "active_skill", "active_point")
                if not registed_skill==input_skill:
                    """スキルに変更有"""
                    if_changed=True
                    diff_skill = input_skill.items() - registed_skill.items()
                    #registed_skillsにあるが、input_skillにないキー
                    diff_skill2 = registed_skill.items() - input_skill.items()
                    omitted_skill=list(dict(diff_skill2).keys() - dict(diff_skill).keys())

                    for skill, point in diff_skill:
                        # print(skill, point)
                        try:
                            ac = SkillDetail.objects.get(active_skill=skill)
                        except SkillDetail.DoesNotExist:
                            ac = SkillDetail(active_skill=skill, active_point=point)
                            ac.save()
                            sb.active_skills.add(ac)
                        else:
                            ac.active_point=point
                            ac.save()

                    for omitted_skill in omitted_skills:
                        ac = SkillDetail.objects.get(active_skill=omitted_skill)
                        sb.active_skills.remove(ac)
                if if_changed:
                    print(sb_data["name"], "更新")
                    sb.save()

        """contain, deactive の更新確認"""
        for sb_data in data:
            """contain"""
            for active_skills in sb_data["active_skills"]:
                if_changed=False
                if active_skills["contain"]:
                    sd = SkillDetail.objects.get(active_skill=active_skills["active_skill"])
                    registed_contain_list = list(sd.contain.all().values_list("active_skill", flat=True))
                    input_contain_list = active_skills["contain"] #contain のリスト
                    registed_contain_set = set(registed_contain_list)
                    input_contain_set = set(input_contain_list)
                    if not input_contain_set==registed_contain_set:
                        if_changed=True
                        """変更あり。未登録のものしか現れない。"""
                        dif_contain = input_contain_set - registed_contain_set
                        for contain in dif_contain:
                            contain_skill=SkillDetail.objects.get(active_skill=contain)
                            sd.contain.add(contain_skill)

                if active_skills["deactive"]:
                    sd = SkillDetail.objects.get(active_skill=active_skills["active_skill"])
                    registed_deactive_list = list(sd.deactive.all().values_list("active_skill", flat=True))
                    input_deactive_list = active_skills["deactive"] #contain のリスト
                    registed_deactive_set = set(registed_deactive_list)
                    input_deactive_set = set(input_deactive_list)
                    if not input_deactive_set==registed_deactive_set:
                        if_changed=True
                        """変更あり。未登録のものしか現れない。"""
                        dif_deactive = input_deactive_set - registed_deactive_set
                        for deactive in dif_deactive:
                            deactive_skill=SkillDetail.objects.get(active_skill=deactive)
                            sd.deactive.add(deactive_skill)
                if if_changed:
                    print(sb_data["name"], "contain, deactive")
                    sb.save()
