from django import forms
from django.core.validators import RegexValidator
from stocks.models import Company, Industry, Market

class CompanyForm(forms.ModelForm):

    name_en = forms.CharField(
        label='会社名（英語）',
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9 ]+$',
                message='会社名（英語）は英字・数字・空白のみ入力可能です。'
            )
        ]
    )
    class Meta:
        model = Company
        fields = ['name_en', 'name_jp', 'industry', 'market', 'memo']
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 1}),
        }
    def clean(self):
        cleaned_data = super().clean()
        name_en = cleaned_data.get("name_en")
        name_jp = cleaned_data.get("name_jp")

        if not name_en and not name_jp:
            raise forms.ValidationError(
                "会社名（英語）または会社名（日本語）のどちらかを入力してください。"
            )

        return cleaned_data        

class CompanySearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '会社名（英語 or 日本語）'})   
    )
    industry = forms.ModelChoiceField(
        queryset=Industry.objects.all(),
        required=False,
        empty_label='業界'
    )
    market = forms.ModelChoiceField(
        queryset=Market.objects.all(),
        required=False,
        empty_label='市場'
    )