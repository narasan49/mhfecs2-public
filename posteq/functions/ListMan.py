"""
ポストされているか確認
"""
def is_eq_post(posts, part):
    try:
        res = posts[part]
    except KeyError:
        res = "スロット3仮装備"
    return res

"""
辞書のデフォルト値指定
"""
def DictWithDefalut(dict, key, default):
    try:
        res=dict[key]
    except KeyError:
        res=default
    return res

def EqDict2SkillList(eq_dict, model):
    stat = True
    mssg = ""
    eqs = []
    for eq in eq_dict:
        try:
            if eq == "wep":
                eqs.append(model.objects.get(data__name=eq_dict[eq]))
            else:
                eqs.append(model.objects.get(data__name=eq_dict[eq], data__part=eq))
        except model.DoesNotExist:
            stat = False
            mssg = eq_dict[eq]+"はデータベースに存在していません。"
            return eqs, stat, mssg
    return eqs, stat, mssg

def JewelDict2SkillList(eq_dict, model):
    stat = True
    mssg = ""
    eqs = []
    for eq in eq_dict:
        for i in range(eq_dict[eq]):
            try:
                print(eq)
                eqs.append(model.objects.get(data__name=eq))
            except model.DoesNotExist:
                stat = False
                res = eq_dict[eq]+"はデータベースに存在していません。"
                return eqs, stat, mssg
    return eqs, stat, mssg
