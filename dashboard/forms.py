from django import forms
from .models import Users, PointsBundle, Posts
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.http import HttpResponse

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
    
import hashlib

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
        print("clean method called")
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                self.add_error('confirm_new_password', "New password and confirm new password do not match.")

        return cleaned_data

    

    def is_valid(self):
        print("is_valid method called")
        return super().is_valid()

    def save(self, *args, **kwargs):
        print("Save method called")
        # Get the user details from the form
        strUserId = self.instance.pk
        strName = self.cleaned_data['name']
        strEmail = self.cleaned_data['email']
        intGender = self.cleaned_data['gender']
        intStatus = self.cleaned_data['status']
        intAgeVerified = self.cleaned_data['age_verified']
        strPassword = self.cleaned_data.get('new_password')

        print("strPassword before update:", strPassword)
        

        # Call the stored procedure to save the user details
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.callproc('sp_Admin_Save_User', [
                strPassword,
                strName,
                strEmail,
                intStatus,
                intGender,
                intAgeVerified,
                strUserId
            ])
            if intAgeVerified == 1:
                subject = '身分証の承認が完了しました。'
                body = '沢山のおしゃべりを楽しんでください！初回特典として、無料メッセージポイントと無料通話ポイントを購入ページから選択できます！'
                email = strEmail
                url = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={subject}&body={body}"
                # Return a JSON response with the URL
                from django.http import JsonResponse
                return JsonResponse({'url': url})
        

        return self.instance
    

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

        