from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

from . import views

urlpatterns = [
    # path('',views.home, name = 'home'),
    path('', views.testing, name='testing'),
    path('register/', views.newregister, name='newregister'),
    path('login/', views.login, name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)