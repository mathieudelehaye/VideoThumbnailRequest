from django import forms
from .models import ThumbnailRequest

class ThumbnailRequestForm(forms.ModelForm):
    class Meta:
        model = ThumbnailRequest
        fields = ['idea', 'reference_image', 'price']
        widgets = {
            'idea': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
