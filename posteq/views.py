from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core import serializers
from posteq.models import (
EQ, EqData, JewelData, CuffData, WepData,
TagBase, WepKind, SkillBase, TeniSkillBase,
SkillInEq, UpdateHist
)
from posteq.forms import PostForm
from posteq.functions.skill import (
    DeriveEquipData, SkillToString, TeniSkillToString, SenyuSkillToString, TagToString,
    CreateEQ
    )
from posteq.functions.misc import EncoArray, DecoArray
from posteq.functions.eqQuery import NarrowdownAddInfo, QueryEqs, JewelRule, CuffRule, IsAlreadyExist, mssg_response
from posteq.functions.ListMan import is_eq_post, DictWithDefalut, EqDict2SkillList, JewelDict2SkillList
from posteq.functions.clip import Clip2EqDict, EqToClip
from posteq import parameters
from user.functions.misc import hash, get_user_from_cookie
import json
import numpy as np
import time
# Create your views here.

class TestView(generic.DetailView):
    model = EqData
    template_name = 'posteq/test.html'

class IndexView(generic.ListView):
    context_object_name = 'hist_list'
    template_name = 'posteq/index.html'

    def get_queryset(self):
        return UpdateHist.objects.order_by('-date')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context

class PostListView(generic.ListView):
    context_object_name = 'posted_list'
    template_name = 'posteq/post_list.html'
    paginated_by = 10
    def get_queryset(self):
        """
        絞り込みや並べ替えの実装
        絞り込み：武器種、タグ、スキル、文字列入力
        """
        order = self.request.GET.getlist('order')
        if "good" in order:
            eqlist = EQ.objects.order_by('-good')
        else:
            eqlist = EQ.objects.order_by('-pos_date')
        """絞り込み(選択)"""
        wep_kind = self.request.GET.getlist('wep_kind')
        tags = self.request.GET.getlist('checked_tags')
        skills = self.request.GET.getlist('skill_kind')
        additional_kind = self.request.GET.getlist('additional_kind')
        additional_num = self.request.GET.getlist('additional_num')
        additional_cond = self.request.GET.getlist('additional_cond')
        if len(additional_kind) > 0:
            eqlist = NarrowdownAddInfo(eqlist, additional_kind, additional_num, additional_cond)

        if len(wep_kind) > 0:
            if wep_kind[0] != "":
                eqlist = eqlist.filter(wep_kind__name=wep_kind[0])
        if len(tags) > 0:
            for tag in tags:
                eqlist = eqlist.filter(tags__name__contains=tag)
        if len(skills) > 0:
            for skill_system in skills:
                # skillbase = SkillBase.objects.get(name=skill_system)
                eqlist = eqlist.filter(active_skills__skill__name__contains=skill_system, active_skills__active="有効")

        """絞り込み(文字列)"""

        """ページネーション"""
        paginator = Paginator(eqlist, 10) # Show 10 per page
        page = self.request.GET.get('page')
        res = paginator.get_page(page)
        return res

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["loggedin"] = loggedin
        context["own"] = own
        context['path_to_list'] = self.request.get_full_path()[6:]
        context['wepkind_list'] = WepKind.objects.all()
        context['tag_list'] = TagBase.objects.all()
        context['skill_list_all'] = SkillBase.objects.order_by('priority')
        info_kinds = ["発動スキル", "使用スロット", "極ラヴィ珠", "真秘伝珠", "祭珠", "イベント珠"]
        info_conds = ["以上", "以下"]
        context['info_kinds'] = info_kinds
        context['info_conds'] = info_conds
        additional = []

        for i in range(len(self.request.GET.getlist('additional_kind'))):
            additional.append( {"kind": self.request.GET.getlist('additional_kind')[i],
                               "num" : self.request.GET.getlist('additional_num')[i],
                               "cond": self.request.GET.getlist('additional_cond')[i]})
        context['additional'] = additional

        selected_order=""
        if len(self.request.GET.getlist('order')) > 0:
            selected_order=self.request.GET.getlist('order')[0]
        context['selected_order'] = selected_order
        skill_type_list = parameters.skill_type_list
        context['skill_type_list']=skill_type_list
        context['skill_list']={}
        for skill_type in skill_type_list:
            context['skill_list'][skill_type] = SkillBase.objects.filter(type=skill_type).order_by('priority')
        return context

class PostEqView(generic.TemplateView):
    template_name = 'posteq/post_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        context['wepkind_list'] = WepKind.objects.all()
        context['skill_list_all'] = SkillBase.objects.order_by('priority')
        context['teniskill_list'] = TeniSkillBase.objects.all()
        context['wepdata_list']  = WepData.objects.all()
        context['tag_list'] = TagBase.objects.all()

        skill_type_list = parameters.skill_type_list
        context['skill_type_list']=skill_type_list
        context['skill_list']={}
        for skill_type in skill_type_list:
            context['skill_list'][skill_type] = SkillBase.objects.filter(type=skill_type).order_by('priority')
        return context

class PostConfirm(generic.FormView):
    form_class = PostForm
    template_name = 'posteq/post_confirm.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context

class PostComplete(generic.TemplateView):
    template_name = 'posteq/post_complete.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context

def SkillQuery(request):
    t0 = time.time()
    selected_skills = dict(request.POST)
    csrf = selected_skills.pop('csrfmiddlewaretoken')

    #なまえ
    try:
        name = selected_skills["name"]
    except KeyError:
        name = ""

    #選択スキルID
    selected_id = []
    try:
        skills = selected_skills["skill_kind"]
    except KeyError:
        res = {"mssg":"スキルを1つ以上選択してください。"}
        res = json.dumps(res)
        return HttpResponse(res,content_type="text/javascript")

    for sk in skills:
        selected_id.append(SkillBase.objects.get(name=sk).id)
    try:
        selected_teniskills = selected_skills["teniskill"]
    except KeyError:
        selected_teniskills = []

    try:
        classes = selected_skills["eq_class"]
    except KeyError:
        res = {"mssg":"その他条件で防具種別を1つ以上選択してください。"}
        res = json.dumps(res)
        return HttpResponse(res,content_type="text/javascript")

    # 武器種選択
    try:
        selected_wep = selected_skills["wep_kind"][0]
    except KeyError:
        res = {"mssg":"武器種を選択してください。"}
        res = json.dumps(res)
        return HttpResponse(res,content_type="text/javascript")
    if selected_wep=="":
        res = {"mssg":"武器種を選択してください。"}
        res = json.dumps(res)
        return HttpResponse(res,content_type="text/javascript")
    gunner=["ライトボウガン", "ヘヴィボウガン", "弓", "ガンナー汎用"]
    if selected_wep in gunner:
        narrowdown_wepkind = ['ガンナー', "共"]
    else:
        narrowdown_wepkind = ['剣士', "共"]

    c = []
    if "辿異防具" in classes:
        c.extend(["ZP", "辿"])
    if "遷悠防具" in classes:
        c.extend(["遷"])
    if "その他G級防具" in classes:
        c.extend(["GP", "GX", "始"])
    # print(selected_skills["teni_level"])
    if selected_skills["teni_level"][0] == "ZX":
        exclude_teni_lower=True
    else:
        exclude_teni_lower=False
    # print(selected_teniskills)
    # print(selected_id)
    queried_eq = QueryEqs(selected_id, EqData, selected_teniskills,
                          classes=c,
                          exclude_teni_lower=exclude_teni_lower,
                          narrowdown_wepkind=narrowdown_wepkind)
    queried_eq.extend(QueryEqs(selected_id, JewelData, selected_teniskills))
    queried_eq.extend(QueryEqs(selected_id, CuffData, selected_teniskills))
    res_time = time.time()-t0
    response = {"data":queried_eq, "time":res_time, "wep_kind":selected_wep, "name":name}
    res = json.dumps(response)
    return HttpResponse(res,content_type="text/javascript")

def PostToEq(request):
    posts = request.POST
    own, loggedin = get_user_from_cookie(request)
    wep_kind=WepKind.objects.get(name=posts["wep_kind"])
    print(posts)
    wep_dict = {}
    eq_dict = {}
    wep_dict["wep"] = is_eq_post(posts, "wep")
    eq_dict["head"] = is_eq_post(posts, "head")
    eq_dict["body"] = is_eq_post(posts, "body")
    eq_dict["arm"]  = is_eq_post(posts, "arm")
    eq_dict["wst"]  = is_eq_post(posts, "wst")
    eq_dict["leg"]  = is_eq_post(posts, "leg")
    jewel_dict={}
    for jewel in posts.getlist("jewel"):
        jewel_dict[jewel] = int(posts["num_"+jewel])
    cuff_dict={}
    for cuff in posts.getlist("cuff"):
        cuff_dict[cuff] = int(posts["num_"+cuff])

    wep, stat, mssg = EqDict2SkillList(wep_dict, WepData)
    if not stat:
        return mssg_response(mssg)
    eqs, stat, mssg = EqDict2SkillList(eq_dict, EqData)
    if not stat:
        return mssg_response(mssg)
    jewels, stat, mssg = JewelDict2SkillList(jewel_dict, JewelData)
    if not stat:
        return mssg_response(mssg)
    cuffs, stat, mssg = JewelDict2SkillList(cuff_dict, CuffData)
    if not stat:
        return mssg_response(mssg)

    stat, mssg = CuffRule(cuffs)
    if not stat:
        return mssg_response(mssg)
    stat, mssg = JewelRule(jewels, wep, eqs)
    if not stat:
        return mssg_response(mssg)
    stat, mssg = IsAlreadyExist(wep_kind, wep, eqs, jewel_dict, cuff_dict)
    if not stat:
        return mssg_response(mssg)

    eqdata = DeriveEquipData(wep, eqs, jewels, cuffs)

    eqdata["wep"] = wep
    eqdata["eqs"] = eqs
    eqdata["jewel_dict"] = jewel_dict
    eqdata["cuff_dict"] = cuff_dict
    eqdata["comment"]=posts["comment"]
    eqdata["tags"]=posts.getlist("checked_tags")
    # print(posts.getlist("checked_tags"), "a")
    eqdata["name"]=DictWithDefalut(posts, "name", "")
    eqdata["wep_kind"]=wep_kind

    skill_str, skill_num = SkillToString(eqdata["skillprops"])
    teniskill_str = TeniSkillToString(eqdata["teniskillprops"])
    senyuskill_str = SenyuSkillToString(eqdata)
    tag_str = TagToString(eqdata["checked_tags"])

    return render(request, 'posteq/post_confirm.html', {"eqdata":EncoArray(eqdata),
                                                        "wep":wep,
                                                        "eqs":eqs,
                                                        "cuffs":cuff_dict,
                                                        "jewels":jewel_dict,
                                                        "skill_str":skill_str,
                                                        "skill_num":skill_num,
                                                        "senyuskill_str":senyuskill_str,
                                                        "teniskill_str":teniskill_str,
                                                        "tag_str":tag_str,
                                                        "comment":eqdata["comment"],
                                                        "own":own,
                                                        "loggedin":loggedin,})
class PostClipView(generic.TemplateView):
    template_name = 'posteq/post_clip.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        context['wepkind_list'] = WepKind.objects.all()
        context['tag_list'] = TagBase.objects.all()
        return context

def ClipToEq(request):
    posts = request.POST
    own, loggedin = get_user_from_cookie(request)
    wep_dict, eq_dict, jewel_dict, cuff_dict = Clip2EqDict(posts["clip"])
    # print(wep_dict, eq_dict, jewel_dict, cuff_dict)

    wep_kind=WepKind.objects.get(name=posts["wep_kind"])
    wep, stat, mssg = EqDict2SkillList(wep_dict, WepData)
    if not stat:
        return mssg_response(mssg)
    eqs, stat, mssg = EqDict2SkillList(eq_dict, EqData)
    if not stat:
        return mssg_response(mssg)
    jewels, stat, mssg = JewelDict2SkillList(jewel_dict, JewelData)
    if not stat:
        return mssg_response(mssg)
    cuffs, stat, mssg = JewelDict2SkillList(cuff_dict, CuffData)
    if not stat:
        return mssg_response(mssg)

    stat, mssg = CuffRule(cuffs)
    if not stat:
        return mssg_response(mssg)
    stat, mssg = JewelRule(jewels, wep, eqs)
    if not stat:
        return mssg_response(mssg)
    stat, mssg = IsAlreadyExist(wep_kind, wep, eqs, jewel_dict, cuff_dict)
    if not stat:
        return mssg_response(mssg)

    eqdata = DeriveEquipData(wep, eqs, jewels, cuffs)

    eqdata["wep"] = wep
    eqdata["eqs"] = eqs
    eqdata["jewel_dict"] = jewel_dict
    eqdata["cuff_dict"] = cuff_dict
    eqdata["comment"]=posts["comment"]
    eqdata["tags"]=posts.getlist("checked_tags")
    eqdata["name"]=DictWithDefalut(posts, "name", "")
    eqdata["wep_kind"]=wep_kind

    skill_str, skill_num = SkillToString(eqdata["skillprops"])
    teniskill_str = TeniSkillToString(eqdata["teniskillprops"])
    senyuskill_str = SenyuSkillToString(eqdata)
    tag_str = TagToString(eqdata["tags"])

    return render(request, 'posteq/post_confirm.html', {"eqdata":EncoArray(eqdata),
                                                        "wep":wep,
                                                        "eqs":eqs,
                                                        "cuffs":cuff_dict,
                                                        "jewels":jewel_dict,
                                                        "skill_str":skill_str,
                                                        "skill_num":skill_num,
                                                        "senyuskill_str":senyuskill_str,
                                                        "teniskill_str":teniskill_str,
                                                        "tag_str":tag_str,
                                                        "comment":eqdata["comment"],
                                                        "own":own,
                                                        "loggedin":loggedin,})

def PostRegister(request):
    posts = request.POST
    own, loggedin = get_user_from_cookie(request)
    eqdata=DecoArray(posts["eqdata"])
    PostedEQ = CreateEQ(eqdata, own)

    return render(request, 'posteq/post_complete.html', {"postedeq":PostedEQ, "own":own, "loggedin":loggedin})

def like(request, pk):
    max_age = 30*24*3600
    eq=EQ.objects.get(id=pk)
    try:
        iines_str = request.COOKIES["iine"]
        if iines_str:
            iines = list(map(int, iines_str.split("--")))
        else:
            iines = []
    except KeyError:
        iines = [pk]
        eq.good += 1
    else:
        if pk in iines:
            eq.good -= 1
            iines.remove(pk)
        else:
            eq.good += 1
            iines.append(pk)
    eq.save()
    iines_map = map(str,iines)
    new_iines_str = '--'.join(iines_map)

    response = json.dumps({'res_good':eq.good,
                           'cookie_to_be_set':new_iines_str,
                           'max_age':max_age,
                           'id':pk})

    return HttpResponse(response,content_type="text/javascript")

def SaveEQ(request):
    id = request.POST["eq_id"]
    eq = EQ.objects.get(id=id)
    own, loggein = get_user_from_cookie(request)
    if eq in own.savedeqs.all():
        own.savedeqs.remove(eq)
        response = json.dumps({'res_text':"保存を取り消しました",
                               'alt_text':"保存する",
                               'src_text':"/static/posteq/images/itembox_not_saved.png",
                               'id':id})
    else:
        own.savedeqs.add(eq)
        response = json.dumps({'res_text':"装備を保存しました",
                               'alt_text':"保存済み",
                               'src_text':"/static/posteq/images/itembox_saved.png",
                               'id':id})
    own.save()
    return HttpResponse(response,content_type="text/javascript")

def SaveToClip(request):
    id = request.POST["eq_id"]
    eq = EQ.objects.get(id=id)
    res = EqToClip(eq)

    response = json.dumps({'res_text':res, "id":id})
    return HttpResponse(response,content_type="text/javascript")

class LinksView(generic.TemplateView):
    template_name = 'posteq/links.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context
