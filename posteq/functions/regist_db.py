from posteq.models import (
    EqData, DataOfEq, Elemental, SkillBase, AbilityInEq, SkillInEq,
    SkillDetail, AbilityDetail
)
import time
def print_time(func):
    def wrapper(*args, **kwargs):
        tt = time.time()
        res = func(*args, **kwargs)
        print(time.time()-tt)
        return res
    return wrapper

def get_or_create_skilldetail(skill, point):
    try:
        sd = SkillDetail.objects.get(active_skill=skill, active_point=point)
    except SkillDetail.DoesNotExist:
        sd = SkillDetail(active_skill=skill, active_point=point)
    return sd

def get_or_create_teniskilldetail(skill, point):
    try:
        sd = AbilityDetail.objects.get(active_skill=skill, active_point=point)
    except AbilityDetail.DoesNotExist:
        sd = AbilityDetail(active_skill=skill, active_point=point)
    return sd

def get_or_create_abilityineq(type, ability):
    try:
        ab_in_eq = AbilityInEq.objects.get(type=type, ability=ability)
    except AbilityInEq.DoesNotExist:
        ab_in_eq = AbilityInEq(type=type, ability=ability)
    return ab_in_eq

def get_or_create_skillineq(skill, point):
    try:
        sk_in_eq = SkillInEq.objects.get(skill=skill, point=point)
    except (SkillInEq.DoesNotExist, ValueError):
        sk_in_eq = SkillInEq(skill=skill, point=point)
    return sk_in_eq

def get_or_create_elemental(elems):
    try:
        res = Elemental.objects.get(fire=elems["fire"],
                         watr=elems["watr"],
                         thnd=elems["thnd"],
                         drgn=elems["drgn"],
                         ice=elems["ice"])
    except Elemental.DoesNotExist:
        res = Elemental(fire=elems["fire"],
                         watr=elems["watr"],
                         thnd=elems["thnd"],
                         drgn=elems["drgn"],
                         ice=elems["ice"])
    return res
def get_or_create_dataofeq(data_of_eq):
    try:
        doe = DataOfEq.objects.get(name=data_of_eq["name"],
                                   part=data_of_eq["part"],
                                   sex=data_of_eq["sex"],
                                   job=data_of_eq["job"],
                                   slot=data_of_eq["slot"],
                                   rare=data_of_eq["rare"],
                                   Class=data_of_eq["Class"],
                                   type=data_of_eq["type"],)
    except DataOfEq.DoesNotExist:
        doe = DataOfEq(name=data_of_eq["name"],
                       part=data_of_eq["part"],
                       sex=data_of_eq["sex"],
                       job=data_of_eq["job"],
                       slot=data_of_eq["slot"],
                       rare=data_of_eq["rare"],
                       Class=data_of_eq["Class"],
                       type=data_of_eq["type"],)
    return doe

def get_or_create_dataofwep(data_of_eq):
    try:
        doe = DataOfEq.objects.get(name=data_of_eq["name"],
                                   part=data_of_eq["part"],
                                   sex=data_of_eq["sex"],
                                   job=data_of_eq["job"],
                                   slot=data_of_eq["slot"],
                                   rare=data_of_eq["rare"],)
    except DataOfEq.DoesNotExist:
        doe = DataOfEq(name=data_of_eq["name"],
                       part=data_of_eq["part"],
                       sex=data_of_eq["sex"],
                       job=data_of_eq["job"],
                       slot=data_of_eq["slot"],
                       rare=data_of_eq["rare"],)
    return doe

def get_or_create_dataofeq_jewel(data_of_eq):
    try:
        doe = DataOfEq.objects.get(name=data_of_eq["name"],
                                   slot=data_of_eq["slot"],
                                   part=data_of_eq["part"],
                                   rare=data_of_eq["rare"],
                                   Class=data_of_eq["Class"],)
    except DataOfEq.DoesNotExist:
        doe = DataOfEq(name=data_of_eq["name"],
                       slot=data_of_eq["slot"],
                       part=data_of_eq["part"],
                       rare=data_of_eq["rare"],
                       Class=data_of_eq["Class"],)
    return doe

def class_assort(d):
    try:
        Class = d.attrib["Class"]
    except KeyError:
        Class = "無分類"

    if Class == "(未)":
        print(d.attrib["Name"]+"は未実装要素です。")
        print("分類を選択してください。")
        print("0:skip, 1:(イ), 2:(イG), 3:(イGX), 4:(祭GX), 5:(GX)")

        select = input("選択:")

        if select == "1":
            Class = "(イ)"
        elif select == "2":
            Class = "(イG)"
        elif select == "3":
            Class = "(イGX)"
        elif select == "4":
            Class = "(祭GX)"
        elif select == "5":
            Class = "(GX)"
        print("区分"+Class+"に登録します。")
    return Class

def dict_registed_data(eq_data, attrib, keys, values):
    registed_data_keys   = list(getattr(eq_data, attrib).all().values_list(keys, flat=True))
    registed_data_values = list(getattr(eq_data, attrib).all().values_list(values, flat=True))
    # print(registed_data_keys, registed_data_values)
    registed_data = dict(zip(registed_data_keys, registed_data_values))
    # print(registed_data)
    return registed_data

def dict_input_data(input_data, type, keys, values):
    """辞書型のリストを辞書型に変換"""
    input_data_keys = [each[keys]for each in input_data[type]]
    input_data_values = [each[values]for each in input_data[type]]
    input_data_dict = dict(zip(input_data_keys, input_data_values))
    return input_data_dict
def dict_input_skill(input_data, type, keys, values):
    """辞書型のリストを辞書型に変換"""
    input_data_keys = [each[keys].name for each in input_data[type]]
    input_data_values = [each[values] for each in input_data[type]]
    input_data_dict = dict(zip(input_data_keys, input_data_values))
    return input_data_dict

def update_if_changed_element(eq_data, eq, if_changed):
    registed_element = eq.element
    elem_keys = ['fire', 'watr', 'thnd', 'drgn', 'ice']
    # registed_element = eq.element
    registed_element_values=[getattr(registed_element, key) for key in elem_keys]
    registed_element_dict = dict(zip(elem_keys, registed_element_values))
    input_element=eq_data["element"]
    # print(registed_element_dict)
    # print(input_element)
    # print(registed_element_dict==input_element)
    if not registed_element_dict==input_element:
        if_changed = True
        elem = get_or_create_elemental(input_element)
        elem.save()
        eq.element = elem
    return eq, if_changed

def update_if_changed_doe(input_doe, registed_doe, doe_keys, if_changed):
    registed_doe_values = [getattr(registed_doe, key) for key in doe_keys]
    registed_doe_dict = dict(zip(doe_keys, registed_doe_values))
    # print(input_doe)
    # print(registed_doe_dict)
    # print(registed_doe_dict==input_doe)
    if not registed_doe_dict==input_doe:
        if_changed = True
        registed_doe.sex = input_doe["sex"]
        registed_doe.job = input_doe["job"]
        registed_doe.slot = input_doe["slot"]
        registed_doe.rare = input_doe["rare"]
        registed_doe.Class = input_doe["Class"]
        registed_doe.type = input_doe["type"]
        registed_doe.save()
    return registed_doe, if_changed
# @print_time
def update_if_changed_ability(eq_data, eq, if_changed):
    registed_abilities = dict_registed_data(eq, "ability", "ability", "type")
    abilities = dict_input_data(eq_data, "ability", "ability", "type")
    # print(registed_abilities, abilities, registed_skills, skills)
    #Ability
    if not abilities==registed_abilities:
        if_changed=True
        #削除されたデータは含まない
        diff_abilities = abilities.items() - registed_abilities.items()
        #registed_abilitiesにあるが、abilitiesにないキー
        diff_abilities2 = registed_abilities.items() - abilities.items()
        omitted_abilities=list(dict(diff_abilities2).keys() - dict(diff_abilities).keys())

        # print(diff_abilities)
        for ability, type in diff_abilities:
            ab_in_eq = get_or_create_abilityineq(type, ability)
            ab_in_eq.save()
            resigted_ab_in_eq = eq.ability.filter(ability=ability)
            if resigted_ab_in_eq.exists():
                eq.ability.remove(resigted_ab_in_eq[0])
            eq.ability.add(ab_in_eq)

        for omitted_ability in omitted_abilities:
            ab_in_eq = get_or_create_abilityineq(registed_abilities[omitted_ability], omitted_ability)
            eq.ability.remove(ab_in_eq)
    return eq, if_changed

def update_if_changed_skill(eq_data, eq, if_changed):
    registed_skills = dict_registed_data(eq, "skills", "skill__name", "point")
    skills = dict_input_skill(eq_data, "skill", "skill", "point")
    # print(registed_abilities, abilities, registed_skills, skills)

    # skill
    if not skills==registed_skills:
        if_changed=True
        diff_skills = skills.items() - registed_skills.items()
        #registed_skillsにあるが、abilitiesにないキー
        diff_skills2 = registed_skills.items() - skills.items()
        omitted_skills=list(dict(diff_skills2).keys() - dict(diff_skills).keys())
        for skillname, point in diff_skills:
            skill = SkillBase.objects.get(name=skillname)
            # print(skill, point)
            sk_in_eq = get_or_create_skillineq(skill, point)
            sk_in_eq.save()
            resigted_sk_in_eq = eq.skills.filter(skill=skill)
            if resigted_sk_in_eq.exists():
                eq.skills.remove(resigted_sk_in_eq[0])
            eq.skills.add(sk_in_eq)
        for omitted_skill in omitted_skills:
            ab_in_eq = get_or_create_abilityineq(registed_skills[omitted_skill], omitted_skill)
            eq.ability.remove(ab_in_eq)
    return eq, if_changed

def create_new_model(eq_data, model, contain_element, contain_ability, contain_skill):
    eq = model()
    eq.save()
    doe = get_or_create_dataofeq(eq_data["data_of_eq"])
    doe.save()
    if contain_element:
        elem = get_or_create_elemental(eq_data["element"])
        elem.save()
        eq.element=elem
    #Ability
    if contain_ability:
        for ab in eq_data["ability"]:
            type=ab["type"]
            ability=ab["ability"]
            ab_in_eq = get_or_create_abilityineq(type, ability)
            ab_in_eq.save()
            eq.ability.add(ab_in_eq)

    # skill
    if contain_skill:
        for ss in eq_data["skill"]:
            skill = ss["skill"]
            point = ss["point"]
            sk_in_eq = get_or_create_skillineq(skill, point)
            sk_in_eq.save()
            eq.skills.add(sk_in_eq)

    print(eq_data["data_of_eq"]["name"], "新規")
    eq.data = doe
    eq.save()
# @print_time
def update_model(eq_data, doe_keys, model,
                 contain_element=True,
                 contain_skill=True,
                 contain_ability=True):
    # print(eq_data)
    """既存かどうかチェック"""
    # tt=time.time()
    try:
        doe = DataOfEq.objects.get(name=eq_data["data_of_eq"]["name"],part=eq_data["data_of_eq"]["part"])
    except DataOfEq.DoesNotExist:
        doe = ""

    if not doe == "":
        # print(eq_data["data_of_eq"]["name"])
        try:
            eq = model.objects.get(data__name=eq_data["data_of_eq"]["name"],data__part=eq_data["data_of_eq"]["part"])
        except model.DoesNotExist:
            """dataはあるが、その親がいない。=>新規の処理をする"""
            create_new_model(eq_data, model, contain_element, contain_ability, contain_skill)
        else:
            if_changed = False
            """elementに変更があるなら反映させる"""
            if contain_element:
                eq, if_changed = update_if_changed_element(eq_data, eq, if_changed)
            """doeに変更があるなら反映させる"""
            doe, if_changed = update_if_changed_doe(eq_data["data_of_eq"], doe, doe_keys, if_changed)
            doe.save()
            # print(if_changed)
            """ ability, skill に変更がある場合に更新する """
            if contain_ability:
                eq, if_changed = update_if_changed_ability(eq_data, eq, if_changed)
            if contain_skill:
                eq, if_changed = update_if_changed_skill(eq_data, eq, if_changed)
            # print(if_changed)
            if if_changed:
                print(eq_data["data_of_eq"]["name"], "変更")
                eq.data = doe
                eq.save()
    else:
        """存在しない:新規"""
        create_new_model(eq_data, model, contain_element, contain_ability, contain_skill)
