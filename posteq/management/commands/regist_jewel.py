from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from ...models import JewelData, DataOfEq, SkillBase, SkillInEq
import numpy as np
from ...functions.regist_db import (
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
        if tmp[-1] == "Jewel.xml":
            model = JewelData
        part="jewel"
        print("import %s" % file)
        # a=JewelData.objects.all()
        # a.delete()
        # a=DataOfEq.objects.filter(part="jewel")
        # a.delete()

        each = {"data_of_eq":{"name":"【空き】",
                              "rare":0,
                              "part":part,
                              "Class":"無分類",
                              "slot":1,
                              "sex":"",
                              "type":"",
                              "job":"",
                              },
                "skill":[],
                }
        """
        <Jewel>
          <Normal>
            <Data Name="ルナ射珠GX3" Job="共" Rare="7" Slot="1" Class="(GX)">
              <Skills>
                  <Skill Point="2">三界の護り</Skill>
                  <Skill Point="3">薬草学</Skill>
                  <Skill Point="3">運気</Skill>
                  <Skill Point="2">調合師</Skill>
              </Skills>
              <Cost Type="create" Money="25000">
                <Item Num="2">金火竜の貫棘</Item>
                <Item Num="1">金火竜の紅玉</Item>
              </Cost>
              <Cost Type="create" Money="25000">
                <Item Num="1">金火竜の兇逆鱗</Item>
              </Cost>
              <Sources>
                  <Source Type="Arm">ルナGXガード</Source>
              </Sources>

        """
        tree = ET.parse(file)
        root = tree.getroot()
        Jewels = root[0]
        data = []
        data.append(each)

        """データ取り出し"""
        for d in Jewels[1000:]:
            # print(d.attrib)
            Class = class_assort(d)
            # skill
            skills = []
            for ss in d[0]:
                skill = SkillBase.objects.get(name=ss.text)
                point = int(ss.attrib["Point"])
                skills.append({"skill":skill, "point":point})

            each = {"data_of_eq":{"name":d.attrib["Name"],
                                  "part":part,
                                  "rare":int(d.attrib["Rare"]),
                                  "Class":Class,
                                  "slot":int(d.attrib["Slot"]),
                                  "sex":"",
                                  "type":"",
                                  "job":"",
                                  },
                    "skill":skills,
                    }
            data.append(each)
        print("データ読み込み完了")
        for eq_data in data:
            doe_keys = ["name", "part", "sex", "job", "slot", "rare", "Class", "type"]
            update_model(eq_data, doe_keys, JewelData, contain_element=False, contain_ability=False)
