from django import forms
from .models import Users, PointsBundle, Posts
from datetime import datetime
from django.utils import timezone
# forms.py
# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = ('profile_pic',)
#         widgets = {
#             'profile_pic': forms.FileInput(),
#         }

    # def save(self, *args, **kwargs):
    #     instance = super(ImageForm, self).save(*args, **kwargs)
    #     # You can add custom logic here if needed
    #     return instance
    
class UserForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    age = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = Users
        fields = ('name', 'email', 'gender', 'status', 'age_verified', 'call_minutes', 'mail_count')

    def __init__(self, *args, **kwargs):
        include_password_fields = kwargs.pop('include_password_fields', True)
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget = forms.Select(choices=[(1, 'Woman'), (0, 'Man')])
        self.fields['age_verified'].widget = forms.Select(choices=[(0, 'Unregistered'), (1, 'Reception Complete'), (2, 'Checking'), (3, 'It was not accepted due to a comprehensive judgement.')])
        if self.instance.dob:
            self.fields['age'].initial = self.calculate_age(self.instance.dob)
        if not include_password_fields:
            self.fields['new_password'].widget = forms.HiddenInput()
            self.fields['confirm_new_password'].widget = forms.HiddenInput()



    def calculate_age(self, dob):
        today = datetime.today()
        
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if self.fields['new_password'].widget != forms.HiddenInput():
            new_password = cleaned_data.get("new_password")
            confirm_new_password = cleaned_data.get("confirm_new_password")

            if new_password != confirm_new_password:
                self.add_error('confirm_new_password', "New password and confirm new password do not match.")
        return cleaned_data
    

class PointsBundleForm(forms.ModelForm):
    class Meta:
        model = PointsBundle
        fields = ('price', 'name', 'description', 'amount', 'percentage', 'promo_percentage', 'sku', 'call_minutes', 'mail_count')
    



# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Posts
#         fields = ('description', 'image')
from django import forms
from .models import Messages

class MessageForm(forms.ModelForm):
    timezone = forms.IntegerField(widget=forms.HiddenInput, initial=1, required=False)  # Add timezone field

    class Meta:
        model = Messages
        fields = ('data', 'timezone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['timezone'].initial = 1  # Set default timezone to 1 (Japan)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.datetime = timezone.now()
        instance.timezone = self.cleaned_data['timezone']  # Set timezone to the value from the form
        if commit:
            instance.save()
        return instance

        