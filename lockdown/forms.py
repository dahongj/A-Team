from django import forms
from .models import AllowlistURL

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = AllowlistURL
        fields = ['url']
        widgets = {
            'url': forms.TextInput(attrs={'placeholder': 'Enter website URL'})
        }