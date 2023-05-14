from django import forms


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

    def __init__(self, request, *args, **kwargs):
        # simply do not pass 'request' to the parent
        super().__init__(*args, **kwargs)
