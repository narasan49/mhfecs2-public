from django.db import models

# Create your models here.
class UpdateHist(models.Model):
    date   = models.DateTimeField('更新日時', null=True)
    datver = models.CharField(max_length=20, null=True, blank=True)
    errors = models.CharField(max_length=1000, null=True, blank=True)
    others = models.CharField(max_length=400, null=True, blank=True)
    def __str__(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S')

class SkillDetail(models.Model):
    active_skill = models.CharField(max_length=20, null=True)
    active_point = models.IntegerField(default=0)
    deactive = models.ManyToManyField("self", blank=True, related_name="deactive_by", symmetrical=False)
    contain  = models.ManyToManyField("self", blank=True, related_name="contained_in", symmetrical=False)

class SkillBase(models.Model):
    name = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=20, null=True)
    priority = models.IntegerField(default=0)
    skillrank = models.IntegerField(default=0)
    active_skills = models.ManyToManyField(SkillDetail, blank=True)

class AbilityDetail(models.Model):
    active_skill = models.CharField(max_length=20, null=True)
    active_point = models.IntegerField(default=0)

class TeniSkillBase(models.Model):
    name = models.CharField(max_length=20, null=True)
    priority = models.IntegerField(default=0)
    active_abilities = models.ManyToManyField(AbilityDetail, blank=True)

class TagBase(models.Model):
    name       = models.CharField(max_length=100, null=True)

class WepKind(models.Model):
    name       = models.CharField(max_length=100, null=True)
    short_name = models.CharField(max_length=100, null=True)

class SkillInEq(models.Model):
    skill = models.ForeignKey(SkillBase, on_delete=models.SET_NULL, null=True)
    point = models.IntegerField(default=0)

class AbilityInEq(models.Model):
    type = models.CharField(max_length=20, null=True)
    ability = models.CharField(max_length=20, null=True)

class DataOfEq(models.Model):
    name = models.CharField(max_length=30, null=True)
    part = models.CharField(max_length=20, null=True)
    sex  = models.CharField(max_length=1, blank=True)
    job  = models.CharField(max_length=4, blank=True)
    slot = models.IntegerField(default=0)
    rare = models.IntegerField(default=0)
    Class= models.CharField(max_length=20, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)

class Elemental(models.Model):
    fire = models.IntegerField(default=0)
    watr = models.IntegerField(default=0)
    thnd = models.IntegerField(default=0)
    drgn = models.IntegerField(default=0)
    ice  = models.IntegerField(default=0)

class EqData(models.Model):
    skills  = models.ManyToManyField(SkillInEq, blank=True)
    ability = models.ManyToManyField(AbilityInEq, blank=True)
    data    = models.ForeignKey(DataOfEq, null=True, blank=True, on_delete=models.SET_NULL)
    element = models.ForeignKey(Elemental, null=True, blank=True, on_delete=models.SET_NULL)

class WepData(models.Model):
    skills  = models.ManyToManyField(SkillInEq, blank=True)
    ability = models.ManyToManyField(AbilityInEq, blank=True)
    """data: class, typeなし"""
    data    = models.ForeignKey(DataOfEq, null=True, blank=True, on_delete=models.SET_NULL)

class CuffData(models.Model):
    skills  = models.ManyToManyField(SkillInEq, blank=True)
    ability = models.ManyToManyField(AbilityInEq, blank=True)
    """
    data: sex, job, typeなし
    """
    data    = models.ForeignKey(DataOfEq, null=True, blank=True, on_delete=models.CASCADE)

class JewelData(models.Model):
    skills  = models.ManyToManyField(SkillInEq, blank=True)
    ability = models.ManyToManyField(AbilityInEq, blank=True)
    """
    data: sex, job, typeなし
    """
    data    = models.ForeignKey(DataOfEq, null=True, blank=True, on_delete=models.CASCADE)

class EqActiveSkill(models.Model):
    skill  = models.ForeignKey(SkillBase, on_delete=models.SET_NULL, null=True)
    point  = models.IntegerField(default=0)
    name   = models.CharField(max_length=100, null=True)
    # 無効、有効、パッシブ
    active = models.CharField(max_length=10, null=True)
class EqActiveTeniSkill(models.Model):
    ability  = models.ForeignKey(TeniSkillBase, on_delete=models.SET_NULL, null=True)
    point  = models.IntegerField(default=0)
    name   = models.CharField(max_length=100, null=True)
class EqActiveAbility(models.Model):
    ability = models.CharField(max_length=20, null=True)
    point  = models.IntegerField(default=0)
    name   = models.CharField(max_length=20, null=True)

class EqVariousData(models.Model):
    tag_str       = models.CharField(max_length=200, null=True, blank=True)
    skill_str     = models.CharField(max_length=300, null=True, blank=True)
    teniskill_str = models.CharField(max_length=200, null=True, blank=True)
    senyuskill_str= models.CharField(max_length=200, null=True, blank=True)

    Nskill     = models.IntegerField(default=0)
    Nslot      = models.IntegerField(default=0)
    NZP        = models.IntegerField(default=0)
    Nkiwami    = models.IntegerField(default=0)
    Nshin      = models.IntegerField(default=0)
    Nfes       = models.IntegerField(default=0)
    Nevent     = models.IntegerField(default=0)
class JewelsInEq(models.Model):
    jewel_data = models.ForeignKey(JewelData, on_delete=models.SET_NULL, null=True)
    num = models.IntegerField(default=1)

class CuffsInEq(models.Model):
    cuff_data = models.ForeignKey(CuffData, on_delete=models.SET_NULL, null=True)
    num = models.IntegerField(default=1)

class EQ(models.Model):
    from user.models import User
    pos_date   = models.DateTimeField('投稿日時', null=True)
    wep_kind   = models.ForeignKey(WepKind, on_delete=models.SET_NULL, null=True)

    wep_data  = models.ForeignKey(WepData, blank=True, null=True, related_name="wep_in_eq", on_delete=models.SET_NULL)
    head_data = models.ForeignKey(EqData, blank=True, null=True, related_name="head_in_eq", on_delete=models.SET_NULL)
    body_data = models.ForeignKey(EqData, blank=True, null=True, related_name="body_in_eq", on_delete=models.SET_NULL)
    arm_data  = models.ForeignKey(EqData, blank=True, null=True, related_name="arm_in_eq", on_delete=models.SET_NULL)
    wst_data  = models.ForeignKey(EqData, blank=True, null=True, related_name="wst_in_eq", on_delete=models.SET_NULL)
    leg_data  = models.ForeignKey(EqData, blank=True, null=True, related_name="leg_in_eq", on_delete=models.SET_NULL)

    jewel_data = models.ManyToManyField(JewelsInEq, blank=True)
    cuff_data = models.ManyToManyField(CuffsInEq, blank=True)

    active_skills    = models.ManyToManyField(EqActiveSkill, blank=True, related_name="active_skills_in_eq")
    active_teni_skills = models.ManyToManyField(EqActiveTeniSkill, blank=True, related_name="active_teni_skills_in_eq")
    active_abilities = models.ManyToManyField(EqActiveAbility, blank=True, related_name="active_abilities_in_eq")

    tags       = models.ManyToManyField(TagBase, blank=True)
    comment    = models.CharField(max_length=400, null=True, blank=True)
    good       = models.IntegerField(default=0)
    data = models.ForeignKey(EqVariousData, blank=True, null=True, on_delete=models.CASCADE)

    posted_user_name = models.CharField(max_length=100, blank=True, null=True)
    posted_user = models.ForeignKey(User, related_name="postedeqs", on_delete=models.CASCADE, blank=True, null=True)
    saved_user = models.ManyToManyField(User, related_name="savedeqs", blank=True)
