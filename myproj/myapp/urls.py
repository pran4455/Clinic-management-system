from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('/register/', views.new_page_view, name='new_page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)