from django.urls import path
from . import views

app_name = "Acount_app"
urlpatterns = [
    path("", views.ProfileUser.as_view(), name="profile"),
    path("edit_profile", views.ProfileEdit.as_view(), name="profile_edit"),
    path("login/", views.LoginView.as_view(), name="Login"),
    path("logout/", views.LogoutView.as_view(), name="Logout"),
    path("register/", views.RegisterView.as_view(), name='Register'),
    path("password_reset", views.PasswordReset.as_view(), name="password_reset"),
    path("password_reset_confirm", views.PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("password_reset_change", views.PasswordResetChange.as_view(), name="password_reset_change"),
    #path("profile/<int:pk>/",views.ProfileTeacher.as_view(),name="profile_teacher"),
    #path("create_teacher",views.CreateTeacher.as_view(),name="create_teacher"),
    path("check_otc/", views.CheckOtc.as_view(), name="check_otc"),

]
