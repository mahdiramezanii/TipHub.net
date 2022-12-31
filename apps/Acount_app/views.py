from django.urls import reverse_lazy,reverse
from django.contrib.auth import logout
from django.views.generic import TemplateView, View,DetailView
from .forms import LoginForm, EditUserForm
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.Acount_app.models import User, Techer
from .mixin import RedirectLogin, CheckLogin
from apps.Acount_app.forms import CreateTeacherForm,OtcForm,CheckOtcForm
from apps.Acount_app.models import Otc
import random
from uuid import uuid4
import ghasedakpack

from django.db.models import Q
from apps.Acount_app.forms import PasswordResetChangeForm


sms = ghasedakpack.Ghasedak("8c1451922c0369b92a8da38aeb7d7b1e75db540b751dc9e30aa5abf61ad9dce7")




class ProfileUser(CheckLogin, TemplateView):
    template_name = "Acount_app/user_panel.html"


class ProfileEdit(View):

    def post(self, request):
        form = EditUserForm(
            request.POST,
            request.FILES,
            instance=request.user)
        if form.is_valid():
            form.save()

            return redirect("Acount_app:profile")
        else:
            return render(request, "Acount_app/edit_user_panel.html", {"form":form})

    def get(self, request):
        form = EditUserForm(instance=request.user)
        return render(request, "Acount_app/edit_user_panel.html", {"form": form})


class PasswordReset(View):

    def post(self,request):

        form=OtcForm(data=request.POST)

        if form.is_valid():

            phone=form.cleaned_data.get("phone")

            if User.objects.filter(phone_number=phone).exists():

                code=random.randint(1000,9999)
                token=uuid4().hex

                # phone = phone
                # sms.verification({'receptor': f'{phone}', 'type': '1', 'template': 'TipHub', 'param1': f'{code}'})
                Otc.objects.create(phone=phone,code=code,token=token)

                return redirect(reverse("Acount_app:password_reset_confirm")+f"?token={token}")
            else:
                form.add_error("phone","کاربر با این شماره موبایل در سایت وجود ندارد!")

        return render(request, "Acount_app/password/password_reset.html", {"form":form})

    def get(self,request):

        form=OtcForm()

        return render(request, "Acount_app/password/password_reset.html", {"form":form})



class PasswordResetConfirm(View):


    def post(self,request):

        form=CheckOtcForm(data=request.POST)

        if form.is_valid():
            token = request.GET.get("token")
            code=form.cleaned_data.get("code")

            if Otc.objects.filter(token=token,code=code).exists():

                otc=Otc.objects.get(token=token)

                if otc.is_expiration_date():

                    return redirect(reverse("Acount_app:password_reset_change")+f"?token={token}")

                else:
                    form.add_error("code","کد وارد شده اعتبار ندارد!")

        return render(request, "Acount_app/password/check_otc_password.html", {"form":form})


    def get(self,request):

        form=CheckOtcForm()

        return render(request, "Acount_app/password/check_otc_password.html", {"form": form})



class PasswordResetChange(View):

    def post(self,request):

        form=PasswordResetChangeForm(data=request.POST)

        if form.is_valid():

            password1=form.cleaned_data.get("password1")

            token=request.GET.get("token")

            otc=Otc.objects.get(token=token)
            user=User.objects.get(phone_number=otc.phone)

            user.set_password(password1)
            user.save()
            otc.delete()
            #login(request,user,backend="Acount_app.authentication.PhoneAuthentication")
            return render(request, "Acount_app/password/password_reset_complete.html")

        return render(request, "Acount_app/password/PasswordResetChange.html", {"form":form})



    def get(self,request):

        form=PasswordResetChangeForm()


        return render(request, "Acount_app/password/PasswordResetChange.html", {"form":form})



"""class PasswordResetRequest(RedirectLogin, View):

    def post(self, request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "Acount_app/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'mahdiramazani.ir',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email,settings.DEFAULT_FROM_EMAIL, [user.email])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")

    def get(self, request):
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="Acount_app/password/password_reset.html",
                      context={"password_reset_form": password_reset_form})"""


"""def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "Acount_app/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")

                
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="Acount_app/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})"""


class LoginView(RedirectLogin, View):
    template_name = "Acount_app/login.html"

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")

            #login with username and phone number
            user=User.objects.get(Q(username=username) | Q(phone_number=username))

            if user.is_active == True:

                user=authenticate(username=username,password=password)

                if user is not None:
                    login(request,user,backend="apps.Acount_app.authentication.PhoneAuthentication")
                    return redirect("Home:Home")
                else:
                    form.add_error("username","نام کاربری یا رمز عبور اشتباه است")
                    return render(request, "Acount_app/login.html", {"form": form})

            else:
                token = uuid4().hex
                code = random.randint(10000, 99999)
                # phone = user.phone_number
                # sms.verification({'receptor': f'{phone}', 'type': '1', 'template': 'TipHub', 'param1': f'{code}'})
                print(code)
                Otc.objects.create(phone=user.phone_number, token=token, code=code)
                return redirect(reverse_lazy("Acount_app:check_otc") + f"?token={token}")

        else:
            form.add_error("username","نام کاربری یا پسورد اشتباه است")

        return render(request, "Acount_app/login.html", {"form": form})

    def get(self, request):
        form = LoginForm()

        return render(request, "Acount_app/login.html", {"form": form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("Home:Home")


# class RegisterView(RedirectLogin, CreateView):
#     template_name = "Acount_app/register.html"
#     form_class = SignupForm
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         current_site = get_current_site(self.request)
#         mail_subject = "فعال سازی حساب شما در تیپ هاب"
#         message = render_to_string('Acount_app/acc_active_email.html', {
#             'user': user,
#             'domain': "mahdiramazani.ir",
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': account_activation_token.make_token(user),
#         })
#         to_email = form.cleaned_data.get('email')
#         email = EmailMessage(
#             mail_subject, message,settings.DEFAULT_FROM_EMAIL, to=[to_email]
#         )
#         email.send()
#         return HttpResponse('لینک فعال سازی برای شما ارسال شد')

class RegisterView(View):

    def post(self,request):

        form=SignupForm(data=request.POST)

        if form.is_valid():

            cd=form.cleaned_data
            user=form.save(commit=False)
            user.is_active=False
            user.set_password(cd.get("password1"))
            user.save()

            #create token for send message
            token=uuid4().hex
            code=random.randint(10000,99999)
            print(code)
            # phone=cd.get("phone_number")
            # sms.verification({'receptor': f'{phone}', 'type': '1', 'template': 'TipHub', 'param1': f'{code}'})
            Otc.objects.create(phone=cd.get("phone_number"),token=token,code=code)

            return redirect(reverse_lazy("Acount_app:check_otc")+f"?token={token}")

        else:
            return render(request, "Acount_app/register.html", {"form":form})

    def get(self,request):
        form=SignupForm()

        return render(request, "Acount_app/register.html", {"form":form})


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect("Acount_app:Login")

    else:
        return HttpResponse('Activation link is invalid!')


class ProfileTeacher(DetailView):
    template_name = "Acount_app/profile.html"
    model = Techer

    def get_context_data(self, **kwargs):
        context = super(ProfileTeacher, self).get_context_data(**kwargs)
        user = self.request.user
        teacher = Techer.objects.get(id=self.object.pk)

        if user in teacher.followers.all():
            context["follow"] = True
        else:
            context["follow"] = False
        return context

    def post(self, request,pk):
        user=request.user
        teacher = Techer.objects.get(pk=pk)


        if user in teacher.followers.all():
            teacher.followers.remove(request.user)

        else:

            teacher.followers.add(request.user)

        return redirect(reverse_lazy("Acount_app:profile_teacher",kwargs={"pk":pk}))


class CreateTeacher(View):

    def post(self,request):
        form=CreateTeacherForm(request.POST,request.FILES)

        if form.is_valid():

            cd = form.cleaned_data
            about_me = cd.get("about_me")
            resume = cd.get("resume")

            if not Techer.objects.filter(user=request.user).exists():
                t=Techer.objects.create(user=request.user)
                t.resume=resume
                t.about_me=about_me
                t.save()
                return redirect("Home:Home")
            return render(request, "Acount_app/create_teacher.html", {"form":form})

    def get(self, request):
        form=CreateTeacherForm()

        return render(request, "Acount_app/create_teacher.html", {"form":form})



class CheckOtc(View):

    def post(self,request):
        form=CheckOtcForm(data=request.POST)

        if form.is_valid():
            token=request.GET.get("token")
            code=form.cleaned_data.get("code")



            if Otc.objects.filter(code=code,token=token).exists():
                otc=Otc.objects.get(token=token)
                if otc.is_expiration_date():
                    user=User.objects.get(phone_number=otc.phone)
                    user.is_active=True
                    user.save()
                    login(request,user,backend="allauth.account.auth_backends.AuthenticationBackend")
                    otc.delete()
                    return redirect("Home:Home")
                else:
                    form.add_error("code","کد وارد شده اعتبار ندراد")
                    return render(request, "Acount_app/check_otc.html", {"form": form})
            else:
                form.add_error("code", "کد نادرست است")
                return render(request, "Acount_app/check_otc.html", {"form": form})

        return render(request, "Acount_app/check_otc.html", {"form":form})

    def get(self,request):

        form=CheckOtcForm()

        return render(request, "Acount_app/check_otc.html", {"form":form})