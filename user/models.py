from django.db import models

# # Create your models here.
class PossessItem(models.Model):
    from posteq.models import EqData, JewelData, CuffData
    possess_equip = models.ManyToManyField(EqData, blank=True)
    possess_jewel = models.ManyToManyField(JewelData, blank=True)
    possess_cuff = models.ManyToManyField(CuffData, blank=True)

class User(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    self_introduce = models.CharField(max_length=400, blank=True, default="")
    access_token = models.CharField(max_length=100, blank=True)
    access_token_secret = models.CharField(max_length=100, blank=True)
    follow = models.ManyToManyField("self", verbose_name="フォロー", blank=True, related_name="followed", symmetrical=False)
    Url = models.URLField(blank=True)
    UrlTitle = models.CharField(max_length=100, blank=True)
    UrlDescription = models.CharField(max_length=400, blank=True)
    UrlIfChecked = models.BooleanField(blank=True, null=True)
    UrlAlertForAdmin = models.BooleanField(default=False)
    possess_item = models.ForeignKey(PossessItem, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
