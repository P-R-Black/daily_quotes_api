from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from quotes_api.models import Quote, Author, Tag
from .serializers import QuotesSerializerV1
import redis
import logging
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.core.cache import cache
from rest_framework.permissions import (
    SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission,
    IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, AllowAny)

from rest_framework import generics
from .mixins import MetadataMixin
from django.conf import settings
from django.utils.text import slugify


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
logger = logging.getLogger(__name__)
logging.basicConfig(filename='daily_quotes.log', level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')



# Create your views here.
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class QuotesListV1(MetadataMixin, generics.ListCreateAPIView):
    permission_classes = [ReadOnly] # [HasAPIKey] [AllowAny]
    queryset = Quote.objects.all()
    serializer_class = QuotesSerializerV1
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # cache.clear()
        cache_key = 'quote_list'
        cache_time = 0
        queryset = cache.get(cache_key)
        logger.debug(f'Daily Quotes/quote_list from cache. Cache hit!!!')

        if not queryset:
            logger.debug(f'Cache miss for Daily Quotes/quote_list data_queryset: fetching data_queryset from database')
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, cache_time)
        logger.debug(f'Returning queryset Daily Quotes/quote_list: {queryset}')

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data
        metadata = self.get_metadata(serialized_data)
        return Response(metadata)


class QuotesByTagV1(MetadataMixin, generics.ListAPIView):
    permission_classes = [ReadOnly]
    serializer_class = QuotesSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self, **kwargs):
        tag = slugify(self.kwargs.get('tag'))

        # Generate a unique cache key based on the base alcohol type
        cache.clear()
        cache_key = f"quote_by_tag_{tag}"
        cache_time = 86400

        # Check if queryset is cached
        queryset = cache.get(cache_key)
        if queryset:
            print('queryset found in cache', queryset)
            logger.debug(f'QuotesByTagV1: cache hit for {cache_key}')
            return queryset

        # If not cached, fetch all tags
        all_tags = Tag.objects.all()
        for item in all_tags.values():
            if slugify(item['name']) == tag:
                tag_lookup = item['id']
                queryset = Quote.objects.filter(tags=tag_lookup).order_by('id')

                # cache result
                cache.set(cache_key, queryset, cache_time)
                logger.debug(f'QuotesByTagV1: data cached for {cache_key}')
                return queryset

        return Quote.objects.none()


    def list(self, request, *args, **kwargs):
        # Fetch the queryset (from cache or DB)
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        # Paginate the data
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_paginated_response(serializer.data)
            metadata = self.get_metadata(paginated_data.data)
            return Response(metadata)

        # if no pagination, return serialized data with metadata
        metadata = self.get_metadata(serialized_data)
        return Response(metadata)


class QuotesByAuthorV1(MetadataMixin, generics.ListAPIView):
    permission_classes = [ReadOnly]
    serializer_class = QuotesSerializerV1
    pagination_class = PageNumberPagination

    def get_queryset(self, **kwargs):
        author = slugify(self.kwargs.get('author'))

        # Generate a unique cache key based on the base alcohol type
        cache.clear()
        cache_key = f"quote_by_tag_{author}"
        cache_time = 0

        # Check if queryset is cached
        queryset = cache.get(cache_key)
        if queryset:
            logger.debug(f'QuotesByTagV1: cache hit for {cache_key}')
            return queryset

        # If not cached, fetch all tags
        all_authors = Author.objects.all()
        for item in all_authors.values():
            if slugify(item['name']) == author:
                author_lookup = item['id']
                queryset = Quote.objects.filter(author=author_lookup).order_by('id')

                # cache result
                cache.set(cache_key, queryset, cache_time)
                logger.debug(f'QuotesByTagV1: data cached for {cache_key}')
                return queryset

        return Quote.objects.none()


    def list(self, request, *args, **kwargs):
        # Fetch the queryset (from cache or DB)
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        # Paginate the data
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_data = self.get_paginated_response(serializer.data)
            metadata = self.get_metadata(paginated_data.data)
            return Response(metadata)

        # if no pagination, return serialized data with metadata
        metadata = self.get_metadata(serialized_data)
        return Response(metadata)