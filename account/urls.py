from django.urls import path
from account.views import Registration,Login,ProfileView, ChangePassword
urlpatterns = [
        path('r/',Registration.as_view(),name="registration"),
        path('l/',Login.as_view(),name="login"),
        path('p/',ProfileView.as_view(),name="profile"),
        path('cp/',ChangePassword.as_view(),name='password-change')
]
