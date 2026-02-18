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
                message='name_enは英字・数字・空白のみ入力可能です。'
            )
        ]
    )

    class Meta:
        model = Company
        fields = ['symbol', 'name_en', 'name_jp', 'industry', 'market', 'memo']
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 1}),
        }
        labels = {
            'symbol': '銘柄コード',
            'name_jp': '会社名（日本語）',
            'industry': '業界',
            'market': '市場',
            'memo': 'メモ',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 銘柄コードは編集不可
        self.fields['symbol'].disabled = True
        

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