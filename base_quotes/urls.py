from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import HomePageView, generate_image


app_name = 'base_quotes'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about', views.about_page, name='about_page'),
    path('docs', views.docs_page, name='docs_page'),
    path('download-image/', views.generate_image, name='download_image'),
    # path('', TemplateView.as_view(template_name="home/home.html")),
]
