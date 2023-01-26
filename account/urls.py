from django.urls import path
from account.views import Registration,Login
urlpatterns = [
        path('r/',Registration.as_view(),name="registration"),
        path('l/',Login.as_view(),name="login"),
]
