from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import HomePageView, AboutPageView, DocsPageView


app_name = 'base_quotes'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about', AboutPageView.as_view(), name='about_page'),
    path('docs', DocsPageView.as_view(), name='docs_page'),
    path('download-image/', views.generate_image, name='download_image'),

]
