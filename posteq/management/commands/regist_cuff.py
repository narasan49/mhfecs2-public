from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from ...models import CuffData, DataOfEq, SkillBase, AbilityInEq, SkillInEq
import numpy as np
from ...functions.regist_db import (
    get_or_create_abilityineq,
    get_or_create_skillineq,
    get_or_create_dataofeq_jewel,
    class_assort,
    update_model,
    )
# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help regist_modelで表示されるメッセージ
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        file = options['file'][0]
        tmp = file.split("/")
        if tmp[-1] == "SkillCuff.xml":
            model = CuffData

        part = "cuff"
        print("import %s" % file)
        a=model.objects.all()
        # for ai in a:
        #     ai.data.part = part
        #     ai.data.save()
        # exit()
        # a.delete()
        each = [{"data_of_eq":{"name":"【空き】",
                               "rare":0,
                               "Class":"無分類",
                               "slot":1,
                               "part":part,
                               "sex":"",
                               "type":"",
                               "job":"",
                              },
                "ability":[],
                "skill":[],
                },
                {"data_of_eq":{"name":"【空き秘伝】",
                               "rare":0,
                               "Class":"無分類",
                               "slot":1,
                               "part":part,
                               "sex":"",
                               "type":"",
                               "job":"",
                              },
                "ability":[],
                "skill":[],
                },
                {"data_of_eq":{"name":"【空き２スロ】",
                               "rare":0,
                               "Class":"無分類",
                               "slot":1,
                               "part":part,
                               "sex":"",
                               "type":"",
                               "job":"",
                              },
                "ability":[],
                "skill":[],
                }
                ]

        """
        <Data Name="砲皇カフ・要塞" Rare="7" Slot="0" Class="(秘)">
          <Abilities>
              <Ability Type="スキル枠消費なし">銃槍技</Ability>
          </Abilities>
          <Skills>
              <Skill Point="12">銃槍技</Skill>
              <Skill Point="3">要塞</Skill>
          </Skills>
          <Cost Type="create" Money="0">
          </Cost>
        </Data>

        """
        tree = ET.parse(file)
        root = tree.getroot()
        data = []
        data.extend(each)

        """データ取り出し"""
        for cuffs in root:
            for d in cuffs:
            # print(d.attrib)
            # Class = class_assort(d)
                try:
                    Class = d.attrib["Class"]
                except KeyError:
                    Class = "無分類"

                #Ability
                abilities = []
                if d[0].tag == "Abilities":
                    ind=1
                    for ab in d[0]:
                        type=ab.attrib["Type"]
                        ability=ab.text
                        abilities.append({"type":type, "ability":ability})
                else:
                    ind=0

                # skill
                skills = []
                for ss in d[ind]:
                    skill = SkillBase.objects.get(name=ss.text)
                    point = int(ss.attrib["Point"])
                    skills.append({"skill":skill, "point":point})

                each = {"data_of_eq":{"name":d.attrib["Name"],
                                      "rare":int(d.attrib["Rare"]),
                                      "Class":Class,
                                      "slot":int(d.attrib["Slot"]),
                                      "part":part,
                                      "sex":"",
                                      "type":"",
                                      "job":"",
                                      },
                        "ability":abilities,
                        "skill":skills,
                        }
                data.append(each)
        print("データ読み込み完了")
        for eq_data in data:
            doe_keys = ["name", "part", "sex", "job", "slot", "rare", "Class", "type"]
            update_model(eq_data, doe_keys, CuffData, contain_element=False)
