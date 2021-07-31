import numpy as np
from posteq.models import SkillBase, TeniSkillBase, SkillInEq, EqData, JewelData, CuffData, WepData, EQ
import collections
from django.db.models import Q
from django.http import HttpResponse
import json

def ExcludeEqs(queryset, selected_teniskills):
    #選択していない辿異スキルを持つ装備を除外
    abbase = TeniSkillBase.objects.exclude(name__in=selected_teniskills) #選択していない辿異スキル
    ab_not_selected = [dic.get("active_abilities__active_skill") for dic in abbase.values("active_abilities__active_skill")]
    queryset = queryset.exclude(ability__ability__in=ab_not_selected)

    return queryset

def QueryEqs(selected_id, model, selected_teniskills,
             classes=None,
             exclude_teni_lower=False,
             narrowdown_wepkind=None,
             ):
    #選択スキルを含む装備
    #複数スキル搭載している装備は複数回呼び出される
    eqdata = model.objects.order_by("-id").filter(Q(skills__skill__id__in=selected_id) | Q(skills__isnull=True))
    # print(len(eqdata))
    if narrowdown_wepkind:
        eqdata = eqdata.filter(data__job__in=narrowdown_wepkind)

    if classes:
        query_by_class = Q(data__Class__contains="未")
        for c in classes:
            # print(c)
            query_by_class = query_by_class | Q(data__Class__contains=c)
            # print(query_by_class)
        eqdata = eqdata.filter(query_by_class)

    if exclude_teni_lower:
        eqdata = eqdata.exclude(Q(data__Class__contains="辿)") | Q(data__Class__contains="辿ZY"))

    if len(selected_teniskills) > 0:
        eqdata = ExcludeEqs(eqdata, selected_teniskills)

    eqdata_ids = list(eqdata.values_list("id", flat=True))
    ##装備id とスキルidのペア: (1,1), (1,2) ...のように装備idは重複
    # filtered_skdata = model.objects.order_by("-id").filter(id__in=eqdata_ids)

    eqid = []
    skid = []
    intval=100
    # print(len(eqdata_ids))
    for i in range(len(eqdata_ids)//intval+1):
        skdata = list(eqdata[i*intval:(i+1)*intval].values("id", "skills__skill__id"))
        eqid.extend([dic.get("id") for dic in skdata])
        skid.extend([dic.get("skills__skill__id") for dic in skdata])
    # print(skdata)
    # eqid = list(eqdata.values_list("id"))
    # skid = list(eqdata.values_list("skills__skill__id"))
    # print(eqid)

    #2次元配列にするための準備
    #n x 5 行列にする
    cnt = collections.Counter(eqid) #各装備のスキル数カウント
    ids = list(cnt.keys())#.sort()
    ids.sort(reverse=True)
    for i in range(len(ids)):
        for j in range(5-cnt[ids[i]]):
            skid.insert(i*5 + cnt[ids[i]]+j, 0)

    # 判別行列：スキル一致数を調べるための行列
    d=np.array(skid).reshape([-1,5])
    # print(d)
    if len(d):
        tmp = np.zeros_like(d)
        for si in selected_id:
            tmp = tmp|(d==si)
        # print(tmp)
        D = np.sum(tmp, axis=1)
        # print(D)

        #一致数による分類
        #zp, zx, gxなどの分類
        #[{id:id, name:name, num:num, Class:Class, part:part}, ...]
        names = []
        classes = []
        parts = []
        intval=100
        # print(len(ids))
        for i in range(len(ids)//intval+1):
            filtered_name = model.objects.order_by("-id").filter(id__in=ids[i*intval:(i+1)*intval]).values("data__name")
            filtered_class = model.objects.order_by("-id").filter(id__in=ids[i*intval:(i+1)*intval]).values("data__Class")
            names.extend([dic.get("data__name") for dic in list(filtered_name)])
            classes.extend([dic.get("data__Class") for dic in list(filtered_class)])
        if model == EqData:
            for i in range(len(ids)//intval+1):
                filtered_part = model.objects.order_by("-id").filter(id__in=ids[i*intval:(i+1)*intval]).values("data__part")
                parts.extend([dic.get("data__part") for dic in list(filtered_part)])
                # parts.extend(list(filtered_eq[i*intval:(i+1)*intval].values_list("data__part", flat=True)))
        elif model == JewelData:
            parts = ["jewel" for i in range(len(ids))]
        elif model == CuffData:
            parts = ["cuff" for i in range(len(ids))]
        elif model == WepData:
            parts = ["wep" for i in range(len(ids))]
        # print(model)
        # print(names)
        result = []
        result.append(ids)
        result.append(names)
        result.append(classes)
        result.append(parts)
        result.append(list(D))
        #転置
        result = [list(x) for x in zip(*result)]
        # result = np.array(result)
        # result = result.transpose()
        # print(np.array(result))
        # print(D)
        # print(len(result))
        D_gt_0 = np.array(result)[(D > 0)]
        sz = np.array(result)[(np.array(classes) == "(S_辿)")]

        res = np.append(D_gt_0, sz, axis=0)
        # print(res.tolist())
        return res.tolist()
    else:
        return []

def NarrowdownAddInfo(eqlist, additional_kind, additional_num, additional_cond):
    for i in range(len(additional_kind)):
        if additional_kind[i] == "発動スキル":
            if additional_cond[i] == "以上":
                eqlist = eqlist.filter(data__Nskill__gte=additional_num[i])
            else:
                eqlist = eqlist.filter(data__Nskill__lte=additional_num[i])
        elif additional_kind[i] == "使用スロット":
            if additional_cond[i] == "以上":
                eqlist = eqlist.filter(data__Nslot__gte=additional_num[i])
            else:
                eqlist = eqlist.filter(data__Nslot__lte=additional_num[i])
        elif additional_kind[i] == "極ラヴィ珠":
            if additional_cond[i] == "以上":
                eqlist = eqlist.filter(data__Nkiwami__gte=additional_num[i])
            else:
                eqlist = eqlist.filter(data__Nkiwami__lte=additional_num[i])
        elif additional_kind[i] == "真秘伝珠":
            if additional_cond[i] == "以上":
                eqlist = eqlist.filter(data__Nshin__gte=additional_num[i])
            else:
                eqlist = eqlist.filter(data__Nshin__lte=additional_num[i])
        elif additional_kind[i] == "祭珠":
            if additional_cond[i] == "以上":
                eqlist = eqlist.filter(data__Nfes__gte=additional_num[i])
            else:
                eqlist = eqlist.filter(data__Nfes__lte=additional_num[i])
        elif additional_kind[i] == "イベント珠":
            if additional_cond[i] == "以上":
                eqlist = eqlist.filter(data__Nevent__gte=additional_num[i])
            else:
                eqlist = eqlist.filter(data__Nevent__lte=additional_num[i])
    return eqlist

"""
枠消費なしは1個以下
スロットは2以下
"""
def CuffRule(cuff_list):
    stat = True
    mssg = ""
    hiden_cuff = 0
    slots = 0
    for cuff in cuff_list:
        abilities = cuff.ability.values()
        for ability in abilities:
            if ability["type"] == "スキル枠消費なし":
                hiden_cuff += 1
        slots += cuff.data.slot

    if hiden_cuff > 1:
        stat = False
        mssg = "秘伝カフは1つまでしか選択できません。"
    if slots > 2:
        stat = False
        mssg = "カフの使用スロットが2を超えています。"
    return stat, mssg

"""
装飾品スロット合計は装備のスロット合計以下
"""
def JewelRule(jewel_list, wep_list, eq_list):
    stat = True
    mssg = ""
    jewel_slots = 0
    eq_slots = 0
    for jewel in jewel_list:
        jewel_slots += jewel.data.slot
    for wep in wep_list:
        eq_slots += wep.data.slot
    for eq in eq_list:
        eq_slots += eq.data.slot

    if jewel_slots > eq_slots:
        stat = False
        mssg = "装備品のスロットが計%dに対して装飾品の使用スロットが%dです。" % (eq_slots, jewel_slots)
    return stat, mssg

def IsAlreadyExist(wep_kind, wep, eqs, jewel_dict, cuff_dict):
    # print(eqs[4])
    stat = True
    mssg = ""
    is_eq_exists=EQ.objects.filter(wep_kind=wep_kind,
                                   wep_data=wep[0],
                                   head_data=eqs[0],
                                   body_data=eqs[1],
                                   arm_data=eqs[2],
                                   wst_data=eqs[3],
                                   leg_data=eqs[4])

    for jewel_name in jewel_dict:
        jewel_query = Q(jewel_data__jewel_data__data__name=jewel_name, jewel_data__num=jewel_dict[jewel_name])
        is_eq_exists.filter(jewel_query)
    for cuff_name in cuff_dict:
        cuff_query = Q(cuff_data__cuff_data__data__name=cuff_name, cuff_data__num=cuff_dict[cuff_name])
        is_eq_exists.filter(cuff_query)
    if is_eq_exists.exists():
        stat = False
        mssg = "すでに同一装備が投稿されています。"
    return stat, mssg

def mssg_response(mssg):
    response = json.dumps({'mssg':mssg})
    return HttpResponse(response,content_type="text/javascript")
