from django.contrib import admin
from quotes_api.models import Quote, Tag, Author


# Register your models here.
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    model = Quote
    list_display = ['text', 'date_posted']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['name',]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author
    list_display = ['name',]
