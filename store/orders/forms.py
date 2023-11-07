from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','address','phone', 'postal_code', 'city']

        # widgets = {'first_name': forms.HiddenInput(),
        #            'last_name': forms.HiddenInput(),
        #           'email': forms.HiddenInput(),}