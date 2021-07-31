import numpy as np
from .models import SkillBase, TeniSkillBase, SkillInEq, EqData, JewelData, CuffData, WepData
import collections
from django.db.models import Q

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
    eqdata = model.objects.order_by("-id").filter(Q(skills__skill__id__in=selected_id) | Q(skills__isnull=True))

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

    filtered_skdata = model.objects.order_by("-id").filter(id__in=eqdata_ids)
    skdata = filtered_skdata.values("id", "skills__skill__id")
    eqid = [dic.get("id") for dic in skdata]
    skid = [dic.get("skills__skill__id") for dic in skdata]

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

    tmp = np.zeros_like(d)
    for si in selected_id:
        tmp = tmp|(d==si)
    # print(tmp)
    D = np.sum(tmp, axis=1)
    # print(D)

    #一致数による分類
    #zp, zx, gxなどの分類
    #[{id:id, name:name, num:num, Class:Class, part:part}, ...]
    filtered_eq = model.objects.order_by("-id").filter(id__in=ids)
    names = list(filtered_eq.values_list("data__name", flat=True))
    classes=list(filtered_eq.values_list("data__Class", flat=True))
    if model == EqData:
        parts = list(filtered_eq.values_list("part", flat=True))
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
    result = np.array(result)
    result = result.transpose()
    D_gt_0 = result[(D > 0)]
    sz = result[(np.array(classes) == "(S_辿)")]

    res = np.append(D_gt_0, sz, axis=0)
    return res.tolist()
def is_eq_post(posts, part):
    try:
        res = posts[part]
    except KeyError:
        res = "スロット3仮装備"
    return res
