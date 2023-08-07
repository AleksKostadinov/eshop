from django import forms
from .models import Account
from .validations import clean_username, clean_password, clean_phone_number, clean_first_name, clean_last_name


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Password'}
        ), validators=[clean_password])

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}
        ))

    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password']


    # validation for password matching
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'

        # Custom validation
        self.fields['username'].validators.append(clean_username)
        self.fields['phone_number'].validators.append(clean_phone_number)
        self.fields['first_name'].validators.append(clean_first_name)
        self.fields['last_name'].validators.append(clean_last_name)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

