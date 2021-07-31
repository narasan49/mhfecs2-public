from django.db import models
from posteq.models import (
    SkillBase, SkillDetail,
    TeniSkillBase, AbilityDetail,
    WepKind,
    EqData, JewelData, CuffData,
    EQ,
)
from user.models import User
# Create your models here.

class RequestedSkill(models.Model):
    skill_base   = models.ForeignKey(SkillBase, on_delete=models.CASCADE)
    skill_detail = models.ForeignKey(SkillDetail, on_delete=models.CASCADE)
    """一致 or 上位"""
    if_greater = models.BooleanField(default=False)

class RequestedTeniSkill(models.Model):
    skill_base   = models.ForeignKey(TeniSkillBase, on_delete=models.CASCADE)
    skill_detail = models.ForeignKey(AbilityDetail, on_delete=models.CASCADE)
    """一致 or 上位"""
    if_greater = models.BooleanField(default=False)

class CallFor(models.Model):
    request_user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_pos_date = models.DateTimeField('投稿日時', null=True)
    wep_kind = models.ForeignKey(WepKind, on_delete=models.SET_NULL, null=True)
    requested_skills     = models.ManyToManyField(RequestedSkill, blank=True)
    requested_teniskills = models.ManyToManyField(RequestedTeniSkill, blank=True)
    request_text = models.CharField(max_length=400, null=True, blank=True)
    if_condition_on = models.BooleanField(default=True) #課金等の条件
    answer_due_date = models.DateTimeField(null=True)
    answers = models.ManyToManyField(EQ, blank=True)
    best_answer = models.ForeignKey(EQ, on_delete=models.CASCADE, blank=True, related_name="best_eq_of")
