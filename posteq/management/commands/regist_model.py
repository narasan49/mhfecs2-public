from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from ...models import EqData, DataOfEq, Elemental, SkillBase, AbilityInEq, SkillInEq
from ...functions.regist_db import (
    get_or_create_abilityineq,
    get_or_create_skillineq,
    get_or_create_elemental,
    get_or_create_dataofeq,
    update_model,
    )

from multiprocessing import Pool
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
        tmp = file.split("/")
        if tmp[-1] == "EquipHead.xml":
            part = "head"
        elif tmp[-1] == "EquipBody.xml":
            part = "body"
        elif tmp[-1] == "EquipArm.xml":
            part = "arm"
        elif tmp[-1] == "EquipWst.xml":
            part = "wst"
        elif tmp[-1] == "EquipLeg.xml":
            part = "leg"

        print("import %s" % file)
        # a=EqData.objects.filter(data__part=part)
        # a.delete()
        # b=DataOfEq.objects.all()
        # b.delete()
        elems = {"fire":0, "watr":0, "thnd":0, "drgn":0, "ice":0}
        each = {"data_of_eq":{"name":"スロット3仮装備",
                              "part":part,
                              "job":"共",
                              "sex":"共",
                              "type":"",
                              "rare":0,
                              "Class":"",
                              "slot":3,
                              },
                "element":elems,
                "ability":[],
                "skill":[],
                }

        """
        <normal>
          <Equip>
            <Data Name="" Sex="" Job="" Rare="" GR="" Class="" Type="">
              <Elemental Fire="" Water="" Thunder="" Ice="" Dragon="" />
              <Level>
              <Abilities>
                  <Ability Type="" />
              <Skills>
                  <Skill Point="">
                  ...
                  <Skill Point="">

        """
        tree = ET.parse(file)
        root = tree.getroot()
        Heads = root[0]

        data = []
        data.append(each)
        """データ取り出し"""
        for d in Heads:
            # print(d[0].attrib)
            element = {}
            element["fire"]=int(d[0].attrib["Fire"])
            element["watr"]=int(d[0].attrib["Water"])
            element["thnd"]=int(d[0].attrib["Thunder"])
            element["drgn"]=int(d[0].attrib["Dragon"])
            element["ice"]=int(d[0].attrib["Ice"])
            #slot
            ## levelの前に強化元情報が入る場合あり
            level_elem = 1 #要素番号
            if d[1].tag != 'Level':
                level_elem += 1
            level7 = d[level_elem][-1]
            slot = int(level7.attrib["Slot"])

            abilities = []
            for ab in d[level_elem+1]:
                type=ab.attrib["Type"]
                ability=ab.text
                abilities.append({"type":type, "ability":ability})

            # skill
            skills = []
            for ss in d[level_elem+2]:
                skill = SkillBase.objects.get(name=ss.text)
                point = int(ss.attrib["Point"])
                skills.append({"skill":skill, "point":point})

            each = {"data_of_eq":{"name":d.attrib["Name"],
                                  "part":part,
                                  "job":d.attrib["Job"],
                                  "sex":d.attrib["Sex"],
                                  "type":d.attrib["Type"],
                                  "rare":int(d.attrib["Rare"]),
                                  "Class":d.attrib["Class"],
                                  "slot":slot,
                                  },
                    "element":element,
                    "ability":abilities,
                    "skill":skills,
                    }
            data.append(each)
        cnt=0
        print("データ読み込み完了")
        # p = Pool(3)
        # res = p.map(update_model,data)
        # p.close()
        # print(data)
        # exit()
        for eq_data in data:
            doe_keys = ["name", "part", "sex", "job", "slot", "rare", "Class", "type"]
            update_model(eq_data, doe_keys, EqData)

            # cnt+=1
            # if cnt>2: exit()
