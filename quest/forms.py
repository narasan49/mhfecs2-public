from django import forms
from .models import CallFor

class PostRequest(forms.ModelForm):
    class Meta:
        model = CallFor
        fields = ("wep_kind",
                  "requested_skills",
                  "requested_teniskills",
                  "request_text",
                  "if_condition_on",
                  "answer_due_date",)
