from django import forms
from django.db import models
from .models import (
    EQ
)


class PostForm(forms.ModelForm):

    class Meta:
        model = EQ
        fields = ("wep_data",
                  "head_data",
                  "body_data",
                  "arm_data",
                  "wst_data",
                  "leg_data",
                  "jewel_data",
                  "cuff_data",
                  "wep_kind",
                  "tags",
                  "comment")
