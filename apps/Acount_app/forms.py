from django import forms
from django.forms import ValidationError
from apps.Acount_app.models import User
from django.core import validators
from django.db.models import Q

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "نام کاربری یا شماره موبایل خود را وارد کنید"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "password-input", "placeholder": "پسورد خود را وارد کنید"}))

    def clean(self):
        username = self.cleaned_data.get("username")

        if not User.objects.filter(Q(username=username) | Q(phone_number=username)).exists():

            raise ValidationError("نام کاربری یا پسورد اشتباه است")


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        "class": "password-input", "placeholder": "لطفا پسورد خود را وارد کنید"
    }))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        "class": "password-input", "placeholder": "لطفا پسورد خود را مجددا وارد کنید"
    }))

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "text-input", "placeholder": "نام کاربری خود را وارد کنید"
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "email-input", "placeholder": "شماره تلفن خود را وارد کنید"
            }),

            "password1": forms.TextInput(attrs={
                "class": "password-input", "placeholder": "لطفا پسورد خود را وارد کنید"
            }),

            "password2": forms.TextInput(attrs={
                "class": "password-input", "placeholder": " پسورد خود را مجددا وارد کنید"
            }),
        }

    def clean(self):

        phone_number=self.cleaned_data.get("phone_number")
        username=self.cleaned_data.get("username")
        password1=self.cleaned_data.get("password1")
        password2=self.cleaned_data.get("password2")


        if User.objects.filter(phone_number=phone_number).exists():

            raise ValidationError("کاربر با این شماره در سایت وجود دارد")

        elif User.objects.filter(username=username).exists():

            raise ValidationError("نام کاربری تکراری است")

        elif password1 != password2 :

            raise ValidationError("دو فیلد گذرواژه با هم مطابقت ندارند")





class EditUserForm(forms.ModelForm):


    class Meta:
        model = User
        fields = ["username", "email", "image", "phone_number", "full_name"]

        widgets={
            "image":forms.FileInput(attrs={
                "class":"btn custom-btn",
                "id":"file-input",
                "type":"file"

            }),
            "full_name":forms.TextInput(attrs={
                "placeholder":"نام و نام خانوادگی خود را وارد کنید"
            }),
            "email":forms.TextInput(attrs={
                "placeholder":"ایمیل خود را وارد کنید"
            }),
            "phone_number":forms.TextInput(attrs={
                "placeholder":"شماره تلفن خود را وارد کنید",

            }),
            "username":forms.TextInput(attrs={
                "placeholder":"نام کاربری خود را وارد کنید"
            })

        }



class CreateTeacherForm(forms.Form):
    resume = forms.FileField()
    about_me = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control"
        })
    )

def check_number(value):

    if value[0] != "0":
        raise ValidationError("شماره تلفن حتما باید با صفر شروع شود!")

    return value

class OtcForm(forms.Form):



    phone=forms.CharField(validators=[
        validators.MaxLengthValidator(12),validators.MinLengthValidator(10),check_number],
        widget=forms.TextInput(attrs={
            "placeholder":"شماره تلفن خود را وارد کنید"
        })
    )

class CheckOtcForm(forms.Form):
    code=forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"کد را وارد کنید"
    }))



class PasswordResetChangeForm(forms.Form):

    password1=forms.CharField(max_length=50,widget=forms.PasswordInput(
        attrs={
            "class": "password-input", "placeholder": "لطفا پسورد خود را وارد کنید"
        }
    ))

    password2=forms.CharField(max_length=50,widget=forms.PasswordInput(
        attrs={
            "class": "password-input", "placeholder": "لطفا پسورد خود را مجددا وارد کنید"
        }
    ))