from django.test import TestCase

# Create your tests here.
from .models import (
    EQ, EqData, JewelData, CuffData,
    TagBase, WepKind, SkillBase, TeniSkillBase,
    SkillInEq
    )
from .functions import QueryEqs
import time

selected_id = [10, 20, 30, 150]
# queried_eq = QueryEqs(selected_id, EqData)
eqdata = EqData.objects.order_by("-id").filter(skills__skill__id__in=selected_id)
eqdata_ids = list(eqdata.values_list("id", flat=True))

t = time.time()
filtered_skdata = EqData.objects.order_by("-id").filter(id__in=eqdata_ids)
skdata = filtered_skdata.values("id", "skills__skill__name")
print(skdata)
print(time.time()-t)

t = time.time()
filtered_skdata = SkillInEq.objects.order_by("-eqdata__id").filter(eqdata__id__in=eqdata_ids)
skdata = filtered_skdata.values("eqdata__id", "skill__name")
print(skdata)
print(time.time()-t)
