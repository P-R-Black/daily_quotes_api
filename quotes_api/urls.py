from django.urls import path
from .views import (QuotesListV1, QuotesByTagV1, QuotesByAuthorV1)

app_name = 'quotes_api'

urlpatterns = [
    path('v1/quotes', QuotesListV1.as_view(), name='all-quotes'),
    path('v1/quotes/<str:tag>', QuotesByTagV1.as_view(), name='quote-by-tag'),
    path('v1/quotes/author/<str:author>', QuotesByAuthorV1.as_view(), name='quote-by-author'),
]