from django.conf.urls import url
from userprofile.api import views

urlpatterns = [
    url(r'^$', views.AuthView.as_view(), name="auth_view"),
]
