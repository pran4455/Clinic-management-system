from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('register/', views.newregister, name='newregister'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.otpsend, name='otpsend')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)