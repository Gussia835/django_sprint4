from .models import Post, Location, Category
from django.contrib import admin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'category',
        'is_published',
    )
    search_fields = (
        'title',
        'text',
    )
    empty_value_display = 'Не задано'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'is_published',
    )
    search_fields = (
        'name',
    )
    empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'slug',
        'title',
    )
    list_filter = (
        'is_published',
    )
    empty_value_display = 'Не задано'
