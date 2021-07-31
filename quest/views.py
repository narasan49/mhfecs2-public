from django.shortcuts import render
from django.views import generic
from user.functions.misc import get_user_from_cookie
from .forms import PostRequest
from posteq.models import (
    WepKind, SkillBase
)
from posteq import parameters

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'quest/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own, loggedin = get_user_from_cookie(self.request)
        context["own"] = own
        context["loggedin"] = loggedin
        return context

class RequestForm(generic.FormView):
    form_class = PostRequest
    template_name = 'quest/requestform.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user, loggedin = get_user_from_cookie(self.request)
        context["user"] = user
        context["loggedin"] = loggedin
        context['wepkind_list'] = WepKind.objects.all()
        context['skill_list_all'] = SkillBase.objects.order_by('priority')
        context['skill_type_list'] = parameters.skill_type_list
        context['skill_list']={}
        for skill_type in parameters.skill_type_list:
            context['skill_list'][skill_type] = context['skill_list_all'].filter(type=skill_type)
        context["skill_detail"]={}
        for sk in context['skill_list_all']:
            context["skill_detail"][sk.name] = []
            for active_skill in sk.active_skills.all().order_by('-active_point'):
                context["skill_detail"][sk.name].append(active_skill.active_skill)

        if not loggedin:
            context["message"]="はじめに会員登録またはログインしてください。"
        return context
