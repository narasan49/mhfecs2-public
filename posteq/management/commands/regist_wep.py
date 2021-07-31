from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from ...models import WepData, DataOfEq, SkillBase, AbilityInEq, SkillInEq
from posteq.functions.regist_db import (
    get_or_create_abilityineq,
    get_or_create_skillineq,
    get_or_create_elemental,
    get_or_create_dataofwep,
    update_model,
    )
# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help regist_wepで表示されるメッセージ
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        #print(args)
        print(options['file'])
        #for file in options['file']:
        file = options['file'][0]
        tmp = file.split("/")
        if tmp[-1] == "Weapon.xml":
            model = WepData
        part="wep"
        print("import %s" % file)
        # eqs=model.objects.all()
        # eqs.delete()
        each = {"data_of_eq":{"name":"スロット3武器",
                              "job":"共",
                              "sex":"共",
                              "rare":0,
                              "slot":3,
                              "part":part,
                              "type":"",
                              "Class":"",
                              },
                "ability":[],
                "skill":[],
                }
        """
        <Weapon>
          <Normal>
            <Data Name="遷悠武器(早食い)" Sex="共" Job="共" Rare="1">
              <Elemental Fire="0" Water="0" Thunder="0" Ice="0" Dragon="0" />
              <Level>
                <L1 Atk="0" Slot="3">
                  <Cost Money="0" />
                </L1>
              </Level>
              <Abilities>
                <Ability Type="スキル発動">早食い</Ability>
              </Abilities>
            </Data>

        """
        tree = ET.parse(file)
        root = tree.getroot()
        Wep = root[0]
        data = []
        data.append(each)
        """データ取り出し"""
        for d in Wep:
            abilities = []
            for ab in d[2]:
                type=ab.attrib["Type"]
                ability=ab.text
                abilities.append({"type":type, "ability":ability})

            each = {"data_of_eq":{"name":d.attrib["Name"],
                                  "part":"wep",
                                  "job":d.attrib["Job"],
                                  "sex":d.attrib["Sex"],
                                  "rare":int(d.attrib["Rare"]),
                                  "slot":int(d[1][0].attrib["Slot"]),
                                  "type":"",
                                  "Class":"",
                                  },
                    "ability":abilities,
                    }
            data.append(each)

        for eq_data in data:
            doe_keys = ["name", "part", "sex", "job", "slot", "rare", "Class", "type"]
            update_model(eq_data, doe_keys, WepData, contain_element=False, contain_skill=False)
            #
            # """既存かどうかチェック"""
            # doe_filt = DataOfEq.objects.filter(name=eq_data["data_of_eq"]["name"],part=eq_data["data_of_eq"]["part"])
            # print(eq_data["data_of_eq"]["name"])
            # if doe_filt.exists():
            #     is_already = True
            #     """doeに変更があるなら反映させる"""
            #     doe = doe_filt[0]
            #     doe.sex = eq_data["data_of_eq"]["sex"]
            #     doe.part = eq_data["data_of_eq"]["part"]
            #     doe.job = eq_data["data_of_eq"]["job"]
            #     doe.slot = eq_data["data_of_eq"]["slot"]
            #     doe.rare = eq_data["data_of_eq"]["rare"]
            # else:
            #     """存在しない"""
            #     is_already = False
            #     doe = get_or_create_dataofwep(eq_data["data_of_eq"])
            # doe.save()
            #
            # if not is_already:
            #     """新規"""
            #     eq = WepData()
            #     eq.save()
            #     #Ability
            #     for ab in eq_data["ability"]:
            #         type=ab["type"]
            #         ability=ab["ability"]
            #         ab_in_eq = get_or_create_abilityineq(type, ability)
            #         ab_in_eq.save()
            #         eq.ability.add(ab_in_eq)
            #
            #     eq.data = doe
            #     eq.save()
            # else:
            #     """変更があるかどうか確認"""
            #     eq = WepData.objects.get(data__name=eq_data["data_of_eq"]["name"],data__part=eq_data["data_of_eq"]["part"])
            #     #Ability
            #     abilities = eq.ability.all().values("type","ability")
            #     for ab in eq_data["ability"]:
            #         type=ab["type"]
            #         ability=ab["ability"]
            #         is_changed=True
            #         for each in abilities:
            #             if (each["type"]==type) and (each["ability"]==ability):
            #                 is_changed=False
            #         if is_changed:
            #             ab_in_eq = get_or_create_abilityineq(type, ability)
            #             ab_in_eq.save()
            #             eq.ability.remove(eq.ability.filter(ability=ability)[0])
            #             eq.ability.add(ab_in_eq)
            #     eq.save()
