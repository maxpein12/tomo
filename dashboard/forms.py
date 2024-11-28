from django import forms
from .models import Client
from .models import Users, PointsBundle

from .models import Posts

# forms.py
class ImageForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('profile_pic',)
        widgets = {
            'profile_pic': forms.FileInput(),
        }

    def save(self, *args, **kwargs):
        instance = super(ImageForm, self).save(*args, **kwargs)
        # You can add custom logic here if needed
        return instance
    
class UserForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Users
        fields = ('name', 'email', 'gender', 'status', 'age_verified', 'call_minutes', 'mail_count')

    def __init__(self, *args, **kwargs):
        include_password_fields = kwargs.pop('include_password_fields', True)
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget = forms.Select(choices=[(1, 'Woman'), (0, 'Man')])
        self.fields['age_verified'].widget = forms.Select(choices=[(0, 'Unregistered'), (1, 'Reception Complete'), (2, 'Checking'), (3, 'It was not accepted due to a comprehensive judgement.')])

        if not include_password_fields:
            self.fields['new_password'].widget = forms.HiddenInput()
            self.fields['confirm_new_password'].widget = forms.HiddenInput()

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
        fields = ('price', 'name', 'description')
    



# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Posts
#         fields = ('description', 'image')