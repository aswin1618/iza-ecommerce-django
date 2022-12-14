from django import forms
from .models import Account,UserProfile,UserAdress

class RegistrationForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
    }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']
        
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "passwords doesn't match!"
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'enter your last name'
        self.fields['email'].widget.attrs['placeholder'] = 'enter your email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'enter your phone number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')
        
      
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
      
            
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)     
   
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
    
class AdressForm(forms.ModelForm):
    
    class Meta:
        model = UserAdress
        fields = ('adress_line_1','adress_line_2','city','state')     
   
    def __init__(self, *args, **kwargs):
        super(AdressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
