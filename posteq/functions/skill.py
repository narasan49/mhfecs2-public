import numpy as np
from ..models import (
    SkillBase, TeniSkillBase, SkillInEq, EqData, JewelData, CuffData, WepData,
    EqVariousData, EQ, EqActiveSkill, EqActiveAbility, EqActiveTeniSkill,
    JewelsInEq, CuffsInEq
    )
import collections
from django.db.models import Q
from django.utils import timezone
from .ListMan import EqDict2SkillList, JewelDict2SkillList

"""
全装備の ability を取得
type ("スキル強化", "Ｇ級効果", "スキル枠拡張", "スキル発動")ごとにまとめる
20190204 "スキル枠消費なし"　追加
"""
def GetAbilities(eq_list):
    res = {"Ｇ級効果":0, "辿異スキル": {}, "スキル発動":{}, "スキル枠消費なし":[]}
    teniskill_dict = {}
    for eq in eq_list:
        abilities = eq.ability.values()
        for ability in abilities:
            abitype = ability["type"]
            if abitype == "Ｇ級効果":
                res["Ｇ級効果"] += 1
            elif abitype == "スキル枠拡張":
                teni_skill = "スキル枠拡張"
                if not teni_skill in res["辿異スキル"]:
                    res["辿異スキル"][teni_skill] = 1
                else:
                    res["辿異スキル"][teni_skill] += 1
            elif abitype == "スキル強化":
                #+1がついていたらそれを削除
                if ability["ability"][-2:] ==  "+1":
                    teni_skill = ability["ability"][:-2]
                else:
                    teni_skill = ability["ability"]

                if not teni_skill in res["辿異スキル"]:
                    res["辿異スキル"][teni_skill] = 1
                else:
                    res["辿異スキル"][teni_skill] += 1
            elif abitype == "スキル発動":
                if not ability["ability"] in res["スキル発動"]:
                    res["スキル発動"][ability["ability"]] = 1
            elif abitype == "スキル枠消費なし":
                res["スキル枠消費なし"].append(ability["ability"])
    return res
"""
有効な teni_skill を検出
return: スキル系列(SkillSystem)、ポイント、発動名の辞書が入った配列
"""
def GetActiveTeniSkills(s_dict):
    res = []
    # print(s_dict)
    for d in s_dict.items():
        teniskillprops={}
        SkillData = TeniSkillBase.objects.get(name=d[0])
        SkillPTdep = SkillData.active_abilities.values()
        #スキル値が0以上のとき
        #d[1] : 装備のポイント
        names = np.array([k["active_skill"] for k in SkillPTdep])
        pts   = np.array([v["active_point"] for v in SkillPTdep])

        system_max = pts.max()
        if system_max > d[1]:
            ind = np.where(pts == d[1])
            active_skill = names[ind][0]
            skill_point = d[1]
        else:
            ind = pts.argmax()
            active_skill = names[ind]
            skill_point = system_max

        teniskillprops["skillsystem"]=d[0]
        teniskillprops["point"]=d[1]
        teniskillprops["skill"]=active_skill
        res.append(teniskillprops)
    return res
"""
skill_point を skill_name ごとに足し合わせる

"""
def SumSkillPoint(eqs):
    skillpoints = {}
    for eq in eqs:
        skills = eq.skills.values("skill__name", "point")
        for skill in skills:
            if skill["skill__name"] in skillpoints:
                skillpoints[skill["skill__name"]] += skill["point"]
            else:
                skillpoints[skill["skill__name"]] = skill["point"]
    skillprops = []
    for sk in skillpoints:
        skillprops.append({"skillsystem":sk,
                           "point":skillpoints[sk]})
    return skillprops
"""
自身を含む上位スキルを検索
skilldata: スキル系統
skill_lowest: 最下位のスキル名
"""
def GetHigherSkills(skillsystem, skill_lowest):
    skilldata = SkillBase.objects.get(name=skillsystem)
    skill_name = skilldata.active_skills.order_by("active_point").values_list("active_skill",flat=True)
    skill_point= skilldata.active_skills.order_by("active_point").values_list("active_point",flat=True)
    ind = list(skill_name).index(skill_lowest)
    res_point = []
    res_name  = []
    for i in range(len(skill_name)):
        if skill_point[i] >= skill_point[ind]:
            res_point.append(skill_point[i])
            res_name.append(skill_name[i])
    return res_name, res_point

"""
有効な skill を検出
return: スキル系列(SkillSystem)、ポイント、発動名の辞書が入った配列

"""
def GetActiveSkills(skillprops):
    res = []
    for skillprop in skillprops:
        skillsystem = SkillBase.objects.get(name=skillprop["skillsystem"])
        skilldetail = skillsystem.active_skills.all().order_by("id")
        names = np.array([k for k in skilldetail.values_list("active_skill", flat=True)])
        pts   = np.array([v for v in skilldetail.values_list("active_point", flat=True)])
        #スキル値が0以上のとき
        if skillprop["point"] >= 0:
            #d[1]を超えない最大値を採用
            pts[pts > skillprop["point"]] = -100000
            if pts.max() > 0:
                ind = pts.argmax()
                active_skill = names[ind]
            else:
                active_skill = "None"
        #スキル値が0未満のとき
        else:
            pts[pts > skillprop["point"]] = 100000
            # print(pts)
            if pts.min() < 0:
                ind = pts.argmin()
                active_skill = names[ind]
            else:
                active_skill = "None"
        if not active_skill == "None":
            skillprop["skill"] = active_skill
            skillprop["contain"] = list(skilldetail[int(ind)].contain.values_list("active_skill", flat=True))
            skillprop["deactive"] = list(skilldetail[int(ind)].deactive.values_list("active_skill", flat=True))
        else:
            skillprop["skill"] = active_skill
            skillprop["contain"] = []
            skillprop["deactive"] = []

        res.append(skillprop)
    return res
"""
最大スキル数、優先順位、競合を検証
最大数：デフォ=10。枠拡張、G級効果の加算を考慮
    20190204 スキル枠消費なし　の該当スキルをカウントしないよう変更
優先順位：SkillBaseのID/10
競合:deactiveに指定があるかどうか。
    xmlの剛撃のdeactivateに攻撃中がない
    ー＞deactivate とそれより下位のスキルを無効にする
        「deactive:攻撃中」の時、攻撃小を無効にしたい
        １．攻撃小の上位スキルを検索
        ２．それらが他のdeactiveに含まれないか検索
    炎寵と青魂の共存を認める
"""
def CheckDeactive(skillprops, abilities):
    indices = []
    for i in range(len(skillprops)):
        if skillprops[i]["skill"] == "None":
            skillprops[i]["active"] = "未発動"
        else:
            skillprops[i]["active"] = "有効"
            indices.append(i)
    n_skill = len(indices)

    #スキル数
     #G級効果
    G_eff = 0
    if abilities["Ｇ級効果"] >= 3:
        G_eff = 1
        if abilities["Ｇ級効果"] == 5:
            G_eff = 2
    #枠拡張
    try:
        skill_extend = abilities["辿異スキル"]["スキル枠拡張"]
    except KeyError:
        skill_extend = 0
    max_number = 10 + G_eff + skill_extend
    """ 20190204: スキル枠消費なしの分スキル枠数追加 """
    if abilities["スキル枠消費なし"]:
        for waku_syouhi in abilities["スキル枠消費なし"]:
            # print(waku_syouhi,skill_system_name)
            # print(skillprops[indices])
            skill_system_names = []
            for ind in indices:
                skill_system_names.append(skillprops[ind]["skillsystem"])
            # skill_system_names = [skillprop["skillsystem"].name for skillprop in skillprops[indices]]
            if waku_syouhi in skill_system_names:
                max_number += 1

    """ スキル枠数制限 """
    if max_number < n_skill:
        #優先順位
        priority = []
        for ind in indices:
            skillsystem = SkillBase.objects.get(name=skillprops[ind]["skillsystem"])
            priority.append(skillsystem.priority)

        sort_ind = np.argsort(priority)
        for i in range(max_number):
            ind = indices[sort_ind[i]]
            skillprops[ind]["active"] = "有効"
        for i in range(max_number,n_skill):
            ind = indices[sort_ind[i]]
            skillprops[ind]["active"] = "無効"
            n_skill -= 1

    indices = []
    for i in range(len(skillprops)):
        if (skillprops[i]["active"] == "有効"):
            indices.append(i)
    n_skill = len(indices)
    #競合

    for i in indices:
        ac = skillprops[i] #発動スキルの候補
        # print(ac)
        #候補とそれより上位のスキルを持ってくる
        highskill_names, highskill_points = GetHigherSkills(ac["skillsystem"], ac["skill"])
        # print(ac["SkillName"])
        for j in indices:
            acj = skillprops[j]
            if j != i:
                for each_highskill_name in highskill_names:
                    """ highskill_namesの中に他のcontainスキルがあれば無効化 """
                    if each_highskill_name in acj["contain"]:
                        ac["active"] = "無効"
                        """
                        喝-10のとき：highskills=[赤魂、青魂]
                        青魂は炎寵のdeactiveは無視するようにする
                        """
                        # print(ac["SkillSystem"], active_skill_list[j]["SkillSystem"])
                        if ((ac["skillsystem"] == "喝") and (acj["skillsystem"] == "炎寵")):
                            ac["active"] = "有効"

                    """他のスキルのdeactiveに無いか検索"""
                    if each_highskill_name in acj["deactive"]:
                        ac["active"] = "無効"

        """遷悠スキルと競合したら無効化"""
        for auto_skill in abilities["スキル発動"]:
            if auto_skill in highskill_names:
                skillprops[i]["active"] = "無効"
    return skillprops
def GetPriority(skillprops):
    for ind in range(len(skillprops)):
        skillsystem = SkillBase.objects.get(name=skillprops[ind]["skillsystem"])
        skillprops[ind]["priority"] = skillsystem.priority
    return skillprops

def DeriveEquipData(wep, eqs, jewels, cuffs):
    abilities = GetAbilities(wep + eqs + cuffs)
    teniskillprops = GetActiveTeniSkills(abilities["辿異スキル"])
    """ [{skillSystem:SkillBase, point:point}, {...}] """
    skillprops = SumSkillPoint(wep + eqs + jewels + cuffs)
    """ [{skillSystem:SkillBase, point:point, skill:"", contain:"", deactive:""}, {...}] """
    skillprops = GetActiveSkills(skillprops)
    """ [{skillSystem:SkillBase, point:point, skill:"", contain:"", deactive:"",active:""}, {...}] """
    skillprops = CheckDeactive(skillprops, abilities)
    """ [{,,,, priority:...}]"""
    skillprops = GetPriority(skillprops)
    res = {"skillprops":skillprops,
           "abilities":abilities,
           "teniskillprops":teniskillprops}
    return res


def SkillToString(skillprops):
    """優先度を取得"""
    priorities = []
    for sp in skillprops:
        priorities.append(sp["priority"])
    sort_priority = np.argsort(priorities)

    active_skills = []
    deactive_skills = []
    for i in range(len(priorities)):
        sp = skillprops[sort_priority[i]]
        if sp["active"] == "有効":
            active_skills.append(sp["skill"])
        elif sp["active"] == "無効":
            deactive_skills.append(sp["skill"])

    skill_str = ""
    for ac in active_skills:
        skill_str += ac + ", "
    if deactive_skills:
        skill_str = skill_str + "("
        for ds in deactive_skills:
            skill_str += ds + ", "
        skill_str = skill_str[0:-2] + ")"
    else:
        skill_str = skill_str[0:-2]
    return skill_str, len(active_skills)
def TeniSkillToString(skillprops):
    skill_str = ""
    # if skillprops["abilities"]["スキル枠拡張"] > 0:
    #     skill_str += "スキル枠拡張+" + str(skillprops["abilities"]["スキル枠拡張"]) + ", "
    for ac in skillprops:
        skill_str += ac["skill"] + ", "
    skill_str = skill_str[0:-2]
    return skill_str

def SenyuSkillToString(skillprops):
    skill_str = ""
    for ac in skillprops["abilities"]["スキル発動"]:
        skill_str += ac + ", "
    skill_str = skill_str[0:-2]
    return skill_str

def TagToString(tags):
    tag_str = ""
    for tag in tags:
        tag_str += tag + ", "
    tag_str = tag_str[0:-2]
    return tag_str

def regist_various_data(eqdata):
    skill_str, skill_num = SkillToString(eqdata["skillprops"])
    teniskill_str = TeniSkillToString(eqdata["teniskillprops"])
    senyuskill_str = SenyuSkillToString(eqdata)
    tag_str = TagToString(eqdata["tags"])

    NZP=0
    for eq in eqdata["eqs"]:
        if "ZP" in eq.data.name:
            NZP += 1
    """
    装飾品情報
    スロット数、極ラヴィ珠数、イベント珠数、祭珠数、真秘伝珠数
    """
    Nslot = 0
    Nkiwami = 0
    Nshin = 0
    Nfes = 0
    Nevent = 0
    for jewel_name in eqdata["jewel_dict"]:
        jewel = JewelData.objects.get(data__name=jewel_name)
        num = eqdata["jewel_dict"][jewel_name]
        Nslot += jewel.data.slot
        if "ラヴィ極" in jewel.data.name:
            Nkiwami += num
        if "真" in jewel.data.name:
            Nshin += num
        if jewel.data.Class in ["(祭G)", "(祭GX)"]:
            Nfes += num
        if jewel.data.Class in ["(イ)", "(イG)", "(イGX)", "(道GX)"]:
            Nevent += num
    res = EqVariousData(tag_str = tag_str,
                        skill_str = skill_str,
                        teniskill_str = teniskill_str,
                        senyuskill_str = senyuskill_str,
                        Nskill = skill_num,
                        Nslot = Nslot,
                        NZP = NZP,
                        Nkiwami = Nkiwami,
                        Nshin = Nshin,
                        Nfes = Nfes,
                        Nevent = Nevent,)
    res.save()
    return res

def regist_active_skills(eqdata, PostedEQ):
    for skillprop in eqdata["skillprops"]:
        try:
            active_skill = EqActiveSkill.objects.get(skill=SkillBase.objects.get(name=skillprop["skillsystem"]),
                                         point=skillprop["point"],
                                         name=skillprop["skill"],
                                         active=skillprop["active"],
                                         )
        except EqActiveSkill.DoesNotExist:
            active_skill = EqActiveSkill(skill=SkillBase.objects.get(name=skillprop["skillsystem"]),
                                         point=skillprop["point"],
                                         name=skillprop["skill"],
                                         active=skillprop["active"],
                                         )
            active_skill.save()
        PostedEQ.active_skills.add(active_skill)
    return PostedEQ

def regist_active_teni_skills(eqdata, PostedEQ):
    for teniskillprop in eqdata["teniskillprops"]:
        try:
            active_teni_skill = EqActiveTeniSkill.objects.get(ability=TeniSkillBase.objects.get(name=teniskillprop["skillsystem"]),
                                                              point=teniskillprop["point"],
                                                              name=teniskillprop["skill"],
                                                              )
        except EqActiveTeniSkill.DoesNotExist:
            active_teni_skill = EqActiveTeniSkill(ability=TeniSkillBase.objects.get(name=teniskillprop["skillsystem"]),
                                                  point=teniskillprop["point"],
                                                  name=teniskillprop["skill"],
                                                  )
            active_teni_skill.save()
        PostedEQ.active_teni_skills.add(active_teni_skill)
    return PostedEQ
def get_or_create_activeability(ability, point, name):
    try:
        active_ability = EqActiveAbility.objects.get(ability=ability, point=point, name=name)
    except EqActiveAbility.DoesNotExist:
        # print("a")
        active_ability = EqActiveAbility(ability=ability, point=point, name=name)
        active_ability.save()
    return active_ability
def regist_active_abilities(eqdata, PostedEQ):
    ab = eqdata["abilities"]
    #res = {"Ｇ級効果":0, "辿異スキル": {}, "スキル発動":{}, "スキル枠消費なし":[]}
    # if ab["Ｇ級効果"]:
        # print(ab["Ｇ級効果"])
    active_ability = get_or_create_activeability("Ｇ級効果", ab["Ｇ級効果"], "")
    PostedEQ.active_abilities.add(active_ability)
    for senyu in ab["スキル発動"]:
        active_ability = get_or_create_activeability("スキル発動",ab["スキル発動"][senyu],senyu)
        PostedEQ.active_abilities.add(active_ability)
    for senyu in ab["スキル枠消費なし"]:
        active_ability = get_or_create_activeability("スキル枠消費なし",1,senyu)
        PostedEQ.active_abilities.add(active_ability)
    return PostedEQ

def CreateEQ(eqdata, own, pos_date=timezone.now()):
    various_data = regist_various_data(eqdata)
    PostedEQ = EQ(wep_kind=eqdata["wep_kind"],
                  wep_data=eqdata["wep"][0],
                  head_data=eqdata["eqs"][0],
                  body_data=eqdata["eqs"][1],
                  arm_data=eqdata["eqs"][2],
                  wst_data=eqdata["eqs"][3],
                  leg_data=eqdata["eqs"][4],
                  comment=eqdata["comment"],
                  data=various_data,
                  pos_date=pos_date,
                  posted_user=own,
                  posted_user_name=eqdata["name"]
                  )
    PostedEQ.save()
    for jewel_name in eqdata["jewel_dict"]:
        jewel = JewelData.objects.get(data__name=jewel_name)
        num = eqdata["jewel_dict"][jewel_name]
        try:
            jewel_in_eq = JewelsInEq.objects.get(jewel_data=jewel, num=num)
        except JewelsInEq.DoesNotExist:
            jewel_in_eq = JewelsInEq(jewel_data=jewel, num=num)
            jewel_in_eq.save()
        PostedEQ.jewel_data.add(jewel_in_eq)
    for cuff_name in eqdata["cuff_dict"]:
        cuff = CuffData.objects.get(data__name=cuff_name)
        num = eqdata["cuff_dict"][cuff_name]
        try:
            cuff_in_eq = CuffsInEq.objects.get(cuff_data=cuff, num=num)
        except CuffsInEq.DoesNotExist:
            cuff_in_eq = CuffsInEq(cuff_data=cuff, num=num)
            cuff_in_eq.save()
        PostedEQ.cuff_data.add(cuff_in_eq)

    PostedEQ = regist_active_skills(eqdata, PostedEQ)
    PostedEQ = regist_active_teni_skills(eqdata, PostedEQ)
    PostedEQ = regist_active_abilities(eqdata, PostedEQ)

    PostedEQ.save()
    return PostedEQ
