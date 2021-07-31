import re
import datetime
"""
クリップから
wep_dict = {"wep":武器名}
eq_dict = {"head":防具名, "body":防具名, ...}
jewel_dict = {"装飾品名": 数量, ...}
cuff_dict = {"カフ名": 数量, ...}
を抽出。
"""
def Clip2EqDict(clip):
    clip_split = clip.split('\n')
    # print(clip_split)
    if len(clip_split) > 0:
        for i in range(len(clip_split)):
            clip_split[i]=clip_split[i].strip()

    while len(clip_split[0]) == 0:
        del clip_split[0]
    ind = 0
    if ("装備クリップ" in clip_split[0]) or ("投稿者" in clip_split[0]):
        ind+=1
    while len(clip_split[ind]) == 0:
        ind+=1
    # print(clip_split)
    clip_eq = []
    clip_jewel = []
    clip_cuff = []
    for i in range(ind,ind+7):
        each_line = clip_split[i]
        each_line = each_line.replace("\u3000", " ")
        each_line = each_line.replace("\t", " ")
        each_line = each_line.replace(",", " ")
        each_line = each_line.replace("○", " ")
        each_line = each_line.replace("●", " ")
        each_line = each_line.replace("★", " ")
        each_line = each_line.replace("☆", " ")
        each_line = each_line.replace("◆", " ")
        each_line = each_line.replace("◇", " ")
        each_line = each_line.replace("-", " ")
        each_line = each_line.replace("－", " ")
        sp = re.split("\ +", each_line)
        start_jewel_ind = 1
        for j in range(1,len(sp)):
            if (sp[j].startswith("(")) and (sp[j].endswith(")")):
                start_jewel_ind += 1
            if (sp[j].startswith("Lv")):
                start_jewel_ind += 1
            if (sp[j].isdigit()):
                start_jewel_ind += 1
        jewel_ind = [j for j in range(start_jewel_ind,len(sp))]

        clip_eq.append(sp[0])
        if i < ind+6:
            for j in jewel_ind:
                if sp[j]:
                    clip_jewel.append(sp[j])
        else:
            for j in jewel_ind:
                if sp[j]:
                    clip_cuff.append(sp[j])

    if "武器スロット" in clip_eq[0]:
        clip_eq[0]="スロット3武器"
    wep_dict = {"wep":clip_eq[0]}
    eq_dict = {"head":clip_eq[1], "body":clip_eq[2], "arm":clip_eq[3], "wst":clip_eq[4], "leg":clip_eq[5]}
    jewel_dict = {}
    for jewel_name in clip_jewel:
        if jewel_name in jewel_dict:
            jewel_dict[jewel_name] += 1
        else:
            jewel_dict[jewel_name] = 1
    cuff_dict = {}
    for cuff_name in clip_cuff:
        if cuff_name in cuff_dict:
            cuff_dict[cuff_name] += 1
        else:
            cuff_dict[cuff_name] = 1

    return wep_dict, eq_dict, jewel_dict, cuff_dict

def EqToClip(eq):
    eq_list = []
    jewel_list = []
    cuff_list = []
    eq_list.append(eq.wep_data.data.name)
    eq_list.append(eq.head_data.data.name)
    eq_list.append(eq.body_data.data.name)
    eq_list.append(eq.arm_data.data.name)
    eq_list.append(eq.wst_data.data.name)
    eq_list.append(eq.leg_data.data.name)

    jewels = eq.jewel_data.all().values("jewel_data__data__name", "num")
    # print(jewels)
    for jewel in jewels:
        jewel_name = jewel["jewel_data__data__name"]
        num = jewel["num"]
        for i in range(num):
            jewel_list.append(jewel_name)
    # print(jewel_list)
    cuffs = eq.cuff_data.all().values("cuff_data__data__name", "num")
    for cuff in cuffs:
        cuff_name = cuff["cuff_data__data__name"]
        num = cuff["num"]
        for i in range(num):
            cuff_list.append(cuff_name)
    res = ""
    pos_time = eq.pos_date + datetime.timedelta(hours=9)
    first_line = eq.wep_kind.name+"(投稿者:"+eq.posted_user_name+"さん, 投稿日時:"+pos_time.strftime('%Y年%m月%d日%H:%M')+")\n\n"
    res+=first_line
    si = 0
    for i in range(6):
        ei = min([si+3,len(jewel_list)])
        jewel_string = ""
        for ji in range(si,ei):
            jewel_string += "　"+jewel_list[ji]
        si = ei
        res += eq_list[i]+"　---"+jewel_string + "\n"
    si = 0
    cuff_string = ""
    for cuff in (cuff_list):
        cuff_string += "　"+cuff
    res += "服Pスロット２　--" + cuff_string + "\n\n"
    res += "[自動発動スキル]"+ "\n"
    res += eq.data.senyuskill_str + "\n"
    res += "[辿異スキル]"+ "\n"
    res += eq.data.teniskill_str + "\n"
    res += "[発動スキル:"+ str(eq.data.Nskill) + "]" + "\n"
    res += eq.data.skill_str + "\n"
    res += "https://nasasan.coresv.com" + "\n"
    return res
