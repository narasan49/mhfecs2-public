from django import template
register = template.Library()

@register.filter
def wepkind_selected(value, querydict):
    wep = querydict.getlist('wep_kind')
    if str(value) in wep:
        return "selected"
    return ""

@register.filter
def selected2(value, value2):
    if value == value2:
        return "selected"
    return ""

@register.filter
def order_selected(value, querydict):
    order = querydict.getlist('order')
    if str(value) in order:
        return "selected"
    return ""

@register.filter
def tag_checked(value, querydict):
    tags = querydict.getlist('checked_tags')
    if str(value) in tags:
        return "checked"
    return ""

@register.filter
def skill_type_selected(value, querydict):
    skills = querydict.getlist('skill_type_select')
    if str(value) in skills:
        return "checked"
    return ""

@register.filter
def skill_checked(value, querydict):
    skills = querydict.getlist('skill_kind')
    if str(value) in skills:
        return "checked"
    return ""

@register.filter
def dict(value, arg, default=""):
    if arg in value.keys():
        return value[arg]
    else:
        return default

@register.simple_tag
def paging(request, page_number):
    querydict = request.GET.copy()
    querydict['page'] = page_number

    return querydict.urlencode()

@register.filter
def jobfilter(value, job):
    value = value.filter(job__in=[job, "共"])
    return value
