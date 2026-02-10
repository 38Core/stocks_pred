from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        label='お名前',
        widget=forms.TextInput()
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'example@email.com'})
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        label='件名',
        widget=forms.TextInput()
    )
    message = forms.CharField(
        required=True,
        label='内容',
        widget=forms.Textarea(attrs={'rows': 10})
    )