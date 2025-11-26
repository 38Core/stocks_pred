from django import forms
from customize.models import FavoriteCompany
from stocks.models import Company

class SimulationForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=None,
        label="会社名"
    )

    start_date = forms.DateField(
        label="開始日",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    end_date = forms.DateField(
        label="終了日",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    initial_invest = forms.IntegerField(
        label="頭金"
    )
    monthly_invest = forms.IntegerField(
        label="月々の掛金"
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ユーザーのお気に入り企業だけ表示
        self.fields['company'].queryset = Company.objects.filter(
            favoritecompany__user=user
        )
        # 表示用ラベルをカスタマイズ（シンボル + 日本名優先/英名）
        self.fields['company'].label_from_instance = lambda obj: f"{obj.symbol} {obj.name_jp or obj.name_en or '名称未設定'}"

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")
        if start and end and end < start:
            self.add_error("end_date", "終了日は開始日より後の日付を入力してください。")
        return cleaned
